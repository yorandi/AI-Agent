import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_path = (
            os.path.commonpath([working_directory_abs, target_path])
            == working_directory_abs
        )
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return str(e)


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a file",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The working directory",
                },
                "file_path": {
                    "type": "string",
                    "description": "The path to the file",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["working_directory", "file_path", "content"],
        },
    },
}
