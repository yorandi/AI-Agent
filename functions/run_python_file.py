import os
import subprocess
from time import time


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None,
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_path = (
            os.path.commonpath([absolute_file_path, working_dir_abs]) == working_dir_abs
        )
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        output = []
        result = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python file",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The working directory",
                },
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "The arguments to pass to the Python file",
                },
            },
            "required": ["working_directory", "file_path"],
        },
    },
}
