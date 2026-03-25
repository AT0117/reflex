import ast
import astor 

class ASTCodeEditor:
    @staticmethod
    def replace_function(filepath, function_name, new_code):
        try:
            with open(filepath, 'r') as file:
                source_code = file.read()
            
            tree = ast.parse(source_code)
            new_func_tree = ast.parse(new_code.strip())
            
            # --- THE FIX: Intelligently search for the function instead of assuming it's on line 1 ---
            new_func_node = None
            for node in new_func_tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    new_func_node = node
                    break
            
            if not new_func_node:
                raise ValueError(f"Function '{function_name}' not found in the AI's generated code.")

            # Locate and replace the node in the original file
            found = False
            for i, node in enumerate(tree.body):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    tree.body[i] = new_func_node
                    found = True
                    break
            
            if not found:
                print(f"AST Error: Function '{function_name}' not found in original file.")
                return False

            modified_source = astor.to_source(tree)
            with open(filepath, 'w') as file:
                file.write(modified_source)
            return True
            
        except Exception as e:
            # We will print the exact error so we can see it in Terminal 2 if it fails
            print(f"\n[AST SURGERY FAILED]: {e}\n") 
            return False