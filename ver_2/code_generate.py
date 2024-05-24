from __future__ import absolute_import, division, print_function, unicode_literals
import openai
import os
from openai import OpenAI
from typing import Union
import matplotlib.pyplot as plt
from backtest_setup import run_cerebro
from data_loader import load_stock_data
from utils import extract_error_message, get_code_from_text, load_base_strategy

# Set environment variables for OpenAI
os.environ["ANYSCALE_API_BASE"] = "https://api.endpoints.anyscale.com/v1"
os.environ["ANYSCALE_API_KEY"] = "esecret_mxhfybv3ehvz954hihatkyqh24"

base_strats = load_base_strategy()

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ['ANYSCALE_API_KEY'],
    base_url=os.environ['ANYSCALE_API_BASE']
)

def chat_query(*args):
    chat_completion = client.chat.completions.create(
        model = "meta-llama/Meta-Llama-3-70B-Instruct",
        messages = [
            {
                "role": "user", "content": args[0]
            }
        ],
        temperature = 0.1
    )
    return chat_completion.choices[0].message.content

def chat_strategy(prompt, base_strats):
    """Generates a new strategy based on the given prompt and base strategy."""
    system = f"""
    You are a python developer that intent to make a workable strategy from human requirement.
    Your task is to create a new BackTestStrategy that follow below msg
    Note: Only return class strategy and change `execute` function only, nothing else


    {prompt}
    And below is the structure of the codebase, you can read the MovingAverageStrategy as an example to make your strategy but only change the `execute` function.
    Please name your class strategy as default name is BackTestStrategy
    ----------------------------
    {base_strats}
    """
    return chat_query(system)

def chat_revise(original_script, revise_prompt=None):
    if revise_prompt:
        revise_system = f"""
        You are a python developer that intends to make a workable strategy from human requirements.
        Your task is to create a new BackTestStrategy that follows the below msg.
        Note: Only return class strategy with your change in execute function.

        Please revise the below script based on requests: {revise_prompt}
        {original_script}
        """
        return chat_query(revise_system)
    else:
        return original_script
    
def generate_and_check_code(prompt, base_strats, func = chat_strategy):
    # code generated by strategy
    generated_code = func(prompt, base_strats)
    # check code
    generated_code, success, error_message = auto_debug_code(generated_code, base_strats)

    return generated_code, success, error_message #, cerebro, thestrats

def auto_debug_code(code, base_strats, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            exec(code, globals())
            cerebro, thestrats = run_cerebro(BackTestStrategy)
            print("Code executed successfully!")
            return code, True, "" #, cerebro, thestrats
        except Exception as e:
            error_message = extract_error_message(e)
            print(f"Attempt {attempt+1} failed with error: {error_message}")

            debug_prompt = f"""
            You are a Python developer and trying to fix the error in the given code.
            The following code has an error:\n\n{code}\n\nError: {error_message}\n\nPlease fix the error.
            Just fix the code following the instruction:
            {base_strats}
            """

            code = chat_query(debug_prompt)
            attempt += 1
    return code, False, "Maximum attempts reached. Code could not be debugged." #, cerebro, thestrats

def main():
    cerebro, thestrats = None, None
    while True:
        # Prompt the user for the initial strategy code generation
        prompt = input("Please provide a prompt for the strategy code generation: ")
        generated_code, success, error_message = generate_and_check_code(prompt, base_strats)

        # If the initial code is successful, print it
        print("Initial strategy code:\n")
        print(generated_code)
        
        while True:
            # Ask the user if they want to revise the strategy code
            revise_prompt = input("Please provide a revision prompt to adjust the strategy code or type 'stop' to finish: ")

            if revise_prompt.lower() == "stop":
                break

            revised_code, success, error_message = generate_and_check_code(revise_prompt, generated_code, chat_revise)

            if not success:
                print(error_message)
            else:
                generated_code = revised_code
                print("Revised strategy executed successfully.")
                print(generated_code)

        stop_execution = input("Do you want to stop? (yes/no): ")
        if stop_execution.lower() == "yes":
            break
    """
    # Print out the final result
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    print("Total point return: ",
    (cerebro.broker.getvalue() - cerebro.broker.startingcash),)

    figs = cerebro.plot(
        iplot=False, 
        style="pincandle", width=60 * 10, height=40 * 10, 
        # dpi=1000
    )
    figs = cerebro.plot(
        iplot=False, style="pincandle", width=32 * 10, height=18 * 10, dpi=300 )
    """
if __name__ == '__main__':
    main()


