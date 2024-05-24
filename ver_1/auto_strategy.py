from __future__ import absolute_import, division, print_function, unicode_literals
import os
import pandas as pd
from openai import OpenAI
from base_strategy import *
import backtrader.strategies as btstrats

# Set environment variables for OpenAI
os.environ["ANYSCALE_API_BASE"] = "https://api.endpoints.anyscale.com/v1"
os.environ["ANYSCALE_API_KEY"] = "esecret_mxhfybv3ehvz954hihatkyqh24"

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ['ANYSCALE_API_KEY'],
    base_url=os.environ['ANYSCALE_API_BASE']
)

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

def debug_code(code_str):
    """Attempts to execute the provided code string and captures errors if any."""
    try:
        exec(code_str)
        print("Code ran successfully.")
        return True, ""
    except Exception as e:
        error_message = str(e)
        print(f"Code execution failed with error: {error_message}")
        return False, error_message

def generate_strategy(prompt, base_strats):
    """Generates a new strategy based on the given prompt and base strategy."""
    system = f"""
    You are a python developer tasked with creating a workable strategy from human requirements.
    {prompt}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": system,
            }
        ],
        model='meta-llama/Meta-Llama-3-70B-Instruct',
    )
    return chat_completion.choices[0].message.content

def revise_strategy(original_script, revise_prompt):
    """Revises the original strategy script based on the provided revision prompt."""
    revise_system = f"""
    You are a python developer tasked with creating a workable strategy from human requirements.
    Your task is to create a new BackTestStrategy that follows the instructions below.
    Note: Only return the class strategy with your changes in the `execute` function.

    Please revise the below script based on the requests: {revise_prompt}
    {original_script}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": revise_system,
            }
        ],
        model="meta-llama/Meta-Llama-3-70B-Instruct",
    )
    return chat_completion.choices[0].message.content

def add_prompt_and_error_messages(prompt, error_message):
    """Adds the prompt and error message to the generated code."""
    adjusted_prompt = f"{prompt}\n\nNote: The following error was encountered when running the code: {error_message}"
    return adjusted_prompt

def generate_and_check_code(prompt, base_strats, func=generate_strategy):
    """Generates and checks the strategy code based on the provided prompt."""
    generated_code = func(prompt, base_strats)
    success, error_message = debug_code(get_code_from_text(generated_code))
    return generated_code, success, error_message

def main():
    # Load the base strategy code
    base_strats = load_base_strategy()

    #prompt = "Please create a strategy that buys when MA1 > MA50, and closes the position after 10 cycles."
    # Please create a strategy that buy when RSI is below 50 and sell when RSI is above 80.
    #revise = "I don't see where you close the position after hold_counter equal 0"
    
    while True:

        # initial code generation from user's input
        prompt = input("Please provide a prompt for the strategy code generation: ")
        # Generate and check the initial code
        generated_code, success, error_message = generate_and_check_code(prompt, base_strats)

        while True:
            if not success:
                # If the initial code fails, regenerate it with the error message
                prompt_with_error = add_prompt_and_error_messages(prompt, error_message)
                # Generate and check the code again
                generated_code, success, error_message = generate_and_check_code(prompt_with_error, base_strats)

            else:
                # If the initial code is successful, print it and break the loop
                print("strategy code:\n")
                print(generated_code)
                break

        while True:
                # Ask the user if they want to revise the strategy code
                revise_prompt = input("Please provide a revision prompt to adjust the strategy code or type 'stop' to finish: ")

                # If the user wants to stop, break the loop
                if revise_prompt.lower() == "stop":
                    break

                # Generate and check the revised code
                revised_code, success, error_message = generate_and_check_code(generated_code, revise_prompt, revise_strategy)

                # If the revised code fails, regenerate it with the error message
                if not success:
                    print(f"Revision attempt failed with error: {error_message}")
                    prompt_with_error = add_prompt_and_error_messages(revise_prompt, error_message)
                    generated_code = revise_strategy(generated_code, prompt_with_error)

                # If the revised code is successful, print it and ask the user if they want to stop
                else:
                    generated_code = revised_code
                    print("Revised strategy executed successfully.")
                    print(generated_code)
        
        stop_execution = input("Do you want to stop? (yes/no): ")
        if stop_execution.lower() == "yes":
            break

if __name__ == '__main__':
    main()
