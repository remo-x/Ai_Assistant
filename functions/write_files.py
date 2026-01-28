import os
from google.genai import types

def write_files(working_directory, file_path, content):
    try:
        
        working_directory_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        
        valid_target_path = (
            os.path.commonpath([working_directory_abs, target_path])
            == working_directory_abs
        )

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        
        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_files",
    description="Write contents in a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The desired content for file."
            )
        },
        required =["file_path","content"]
    ),
)