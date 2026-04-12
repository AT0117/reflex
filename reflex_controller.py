import os
from datetime import datetime
from crewai import Agent, Task, Process, Crew
from crewai.tools import tool
from dotenv import load_dotenv
import ast_code_editor

# --- TOOL 1: THE EYES ---
@tool("DocReader_Tool")
def read_documentation_tool(filepath: str) -> str:
    """Reads a local documentation or markdown file to find the latest API schema rules."""
    print(f"\n---> [EYES] Reading documentation file: {filepath} <---")
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading docs: {e}"

# --- TOOL 2: THE MUSCLE (WITH SANITIZER) ---
@tool("CodeEditor_Tool")
def code_editor_tool(filepath: str, function_name: str, healed_function_code: str) -> str:
    """Uses Python's ast module to surgically rewrite a specific function within a file."""
    print(f"\n---> [MUSCLE] Executing AST tool on {filepath}:{function_name} <---")
    
    clean_code = healed_function_code.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code[9:]
    elif clean_code.startswith("```"):
        clean_code = clean_code[3:]
    if clean_code.endswith("```"):
        clean_code = clean_code[:-3]
    clean_code = clean_code.strip()
    
    editor = ast_code_editor.ASTCodeEditor()
    success = editor.replace_function(filepath, function_name, clean_code)
    
    if success:
        return "Successfully edited file."
    else:
        return "Failed to edit file. The code had invalid syntax or missing 'def' statement."

# --- TOOL 3: THE PEN ---
@tool("Logger_Tool")
def log_change_tool(log_message: str) -> str:
    """Appends a summary of code changes made by the agent to logs.txt."""
    print(f"\n---> [PEN] Writing audit trail to logs.txt <---")
    try:
        with open("logs.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] PROJECT REFLEX AUTONOMOUS PATCH:\n{log_message}\n")
            f.write("-" * 50 + "\n")
        return "Successfully logged the change."
    except Exception as e:
        return f"Error writing log: {e}"


class ReflexBrainController:
    def __init__(self):
        load_dotenv()
        if not os.environ.get("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

    def heal_api_integration(self, error_traceback, target_file, target_function):
        with open(target_file, 'r') as file:
            current_code = file.read()
        
        sre_agent = Agent(
            role="Reflex Senior Site Reliability Engineer Agent",
            goal="Investigate API failures by reading documentation, write a code patch, and log the audit trail.",
            backstory="You are an autonomous SRE. You read docs to find schema changes, fix the code, and always log your work.",
            llm="gemini/gemini-2.5-flash-lite", 
            tools=[read_documentation_tool, code_editor_tool, log_change_tool],
            verbose=True,
            allow_delegation=False
        )
        
        healing_task_prompt = f"""
            ### CONTEXT: CRITICAL API FAILURE
            Target File: `{target_file}`
            Function to Heal: `{target_function}`
            HTTP Error Traceback: \n{error_traceback}
            Current Broken Code: \n```python\n{current_code}\n```

            ### MISSION (YOU MUST COMPLETE THESE 3 STEPS IN ORDER):
            1. **RESEARCH:** Use the `DocReader_Tool` to read `documentation.md`. Find out what the new JSON key requirements are for the external API.
            2. **FIX CODE:** Based on the documentation, synthesize the corrected Python function. Use the `CodeEditor_Tool` to rewrite `{target_function}` in `{target_file}`. The new code must be valid Python.
            3. **AUDIT LOG:** Use the `Logger_Tool` to write a brief, professional summary of the exact variable change you made so human engineers know what happened.

            ### OUTPUT FORMAT REQUIREMENT:
            Return a final success message only after all three tools have returned success.
            """

        healing_task = Task(
            description=healing_task_prompt,
            agent=sre_agent,
            expected_output="Confirmation that docs were read, code was patched, and the log was written."
        )
        
        reflex_crew = Crew(
            agents=[sre_agent],
            tasks=[healing_task],
            process=Process.sequential
        )
        
        print(f"\n[BRAIN] Orchestrating Reflex Agent for the target function named {target_function}...")
        return reflex_crew.kickoff()