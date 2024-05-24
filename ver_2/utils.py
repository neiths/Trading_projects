def get_code_from_text(text):
    """Extracts the Python code segment from the provided text."""
    code_segment = text.split("```")[1]
    if "```python" in text:
        code_segment = code_segment[6:]
    return code_segment.strip()

def load_base_strategy():
    """Loads the base strategy code from the base_strategy.py file."""
    with open("base_strategy.py", "r") as f:
        base_strats = f.read()
    return base_strats

def extract_error_message(error):
    error_lines = str(error).split('\n')
    for line in error_lines:
        if 'Error' in line or 'Exception' in line:
            return line.strip()
    return error_lines[-1].strip()

