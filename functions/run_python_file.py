import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
   try:
      # 
        working_directory_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        valid_target_path = (
            os.path.commonpath([working_directory_abs, target_path])
            == working_directory_abs
        )

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not completed_process.stdout and not completed_process.stderr:
            output_parts.append("No output produced")
        else:
            if completed_process.stdout:
                output_parts.append('STDOUT: ' + completed_process.stdout)
            
            if completed_process.stderr:
                output_parts.append('STDERR: '+ completed_process.stderr)
        result = "\n".join(output_parts)
        return result

    
   except Exception as e:
      return f"Error: executing Python file: {e}"
   

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },
        required=["file_path"],  
    ),
)