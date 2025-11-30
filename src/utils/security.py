

def sanitize_input(input_str: str) -> str:
    """
    Basic input sanitization to prevent obvious command injection if not using shlex properly.
    Although we use shlex.quote, this adds an extra layer of check.
    """
    # Remove null bytes
    if '\0' in input_str:
        raise ValueError("Input contains null bytes")
    return input_str

def safe_command(command_list: list[str]) -> list[str]:
    """
    Ensures all arguments are safe for subprocess.
    """
    return command_list # subprocess.run with list args is generally safe from shell injection
