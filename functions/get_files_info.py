import os
from google.genai import types

def get_files_info(working_directory, directory="."):
   try:
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs,directory))
    valid_target_dir = os.path.commonpath([working_directory_abs,target_dir]) == working_directory_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    item_list = []
    for item in os.listdir(target_dir):
        full_item_path = os.path.join(target_dir,item)
        item_size = os.path.getsize(full_item_path)
        is_it_dir = os.path.isdir(full_item_path)
        item_list.append(f'- {item}: file_size={item_size} bytes, is_dir={is_it_dir}')                      
    return "\n".join(item_list)
   except Exception as e:
      return f"Error: {e}"
   

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

