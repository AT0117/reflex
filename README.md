### Project Reflex ###

<br>
Project Reflex is an automated self-healing application that allows the system to recover from external API schema changes by dynamically rewriting its own integration code. <br>
Systems can intercept HTTP errors prior to failure as well as see autonomous code correction executed via Abstract Syntax Trees (AST).

### Preview ###

https://youtu.be/aw4ArZNAAPc?si=PZXyzoA2azn8G4CD

### Environment Setup ###
<ol>
  <li>Ensure Python 3.11+ is installed on the system.</li>
  <li>Create and activate a Python virtual environment (<code>python -m venv venv</code> and <code>source venv/bin/activate</code>).</li>
  <strong>IMPORTANT: This step is mandatory for Arch Linux environments to comply with PEP 668.</strong>
  <li>Dependencies: Install required packages -> <code>pip install fastapi uvicorn requests crewai python-dotenv langchain-google-genai astor</code>.</li>
  <li>Credentials: Create a <code>.env</code> file in the root directory -> add <code>GEMINI_API_KEY="insert_api_key_here"</code>.</li>
</ol>
<br>
Execute these commands in separate terminal sessions - <br>

```bash
# 1. Initialize the Mock External API (Terminal 1)
python mock_external_api.py

# 2. Initialize the Main Application (Terminal 2)
python main_application.py

# 3. Trigger the System Failure (Terminal 3)
curl [http://127.0.0.1:8000/get-user-profile/123](http://127.0.0.1:8000/get-user-profile/123)

# 4. Reset the Environment (Post-Execution)
# The system permanently modifies api_integration.py upon successful healing.
# Manually revert 'account_id' back to 'user_id' in api_integration.py before subsequent runs.
