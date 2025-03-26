import numpy as np
import sys
import os
import re
import json
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

NUM_TEST_CASES = 5
NUM_BATCHES = 2

load_dotenv()

def generate_test_input(low: int, high: int, type: str):
    if type == "int":
        test_input = int(np.random.randint(low, high, size=1)[0])
    elif type == "float":
        test_input = float(np.random.uniform(low, high, size=1)[0])

    return test_input

def generate_test_cases(model_output: dict, num_test_cases: int, num_batches: int, problem_editorial):
    test_cases = []

    for i in range(num_batches):
        for j in range(num_test_cases):
            curr = model_output["input_specifications"]
            test_case = {
                "batch": i + 1,
                "case": j + 1,
                "inputs": [],
                "output": ""
            }

            for problem_input in curr:
                if problem_input["type"] != "int" and problem_input["type"] != "float":
                    raise Exception("Invalid input type. We currently only support int and float")

                else:
                    test_case["inputs"].append(
                        str(generate_test_input(
                            problem_input["low"], 
                            problem_input["high"], 
                            problem_input["type"]
                        ))
                    )
            
            test_output = generate_test_output('\n'.join(test_case["inputs"]), problem_editorial)
            test_case["output"] = test_output

            test_cases.append(test_case)
        
    return test_cases

def generate_test_output(input_data: str, problem_editorial):
    result = subprocess.run(
        [sys.executable, problem_editorial],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=2,
    )

    if not result.stdout or result.stderr:
        raise Exception(f"Error: {result.stderr}")
    
    actual_output = result.stdout.strip()

    return actual_output

def create_test_files(test_cases: list, problem_id: str):
    folder_path = os.path.join('tests', problem_id)
    os.makedirs(folder_path)

    for test_case in test_cases:
        file_name = f"{test_case['batch']}-{str(test_case['case']).zfill(2)}"

        input_file = os.path.join('tests', problem_id, file_name + '.in')
        output_file = os.path.join('tests', problem_id, file_name + '.out')

        input_data = '\n'.join(test_case['inputs'])
        output_data = test_case['output']

        with open(input_file, 'w') as infile:
            infile.write(input_data)
        
        with open(output_file, 'w') as outfile:
            outfile.write(output_data)
        
        print(f"Batch {test_case['batch']} test case {test_case['case']} generated")

def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python test.py <problem_id>")

            sys.exit(1)

        problem_id = sys.argv[1]
        problem_unit = "Unit-" + problem_id.split("-")[0]
        problem_chapter = "Chapter-" + problem_id.split("-")[1]

        problem_statement = os.path.join(problem_unit, problem_chapter, problem_id + ".md")
        problem_editorial = os.path.join(problem_unit, problem_chapter, problem_id + ".py")

        if not problem_statement or not problem_editorial:
            raise Exception("Problem statement or editorial not found")

        with open(problem_statement, "r", encoding="utf-8") as file:
            problem_statement_content = file.read()

        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "system", 
                "content": '''
                    You are a helpful assistant for a computer science class. 
                    In the computer science class, we give students problems to solve.

                    You are given a problem statement and an editorial for a problem. 
                    You need to extract the input types for the problem based off of the problem statement's input specification.
                    The problem statement will provide constraints and the data type for each input in markdown.
                    Your response will be a json schema that provides the extracted data type and bounds if applicable.

                    Example problem statement input specification:

                    ```
                    ## Input Specification  
                    The line of input contains a number, *N*, where `-1000000 ≤ N ≤ 1000000`.
                    ```

                    Your output:
                    "input_specifications": {
                        [
                            {
                                "type": "float", # or "int"
                                "low": -1000000,
                                "high": 1000000,
                            }
                        ]
                    }
                '''
                },
                {
                    "role": "user", 
                    "content": "Problem statement: " + problem_statement_content
                },
            ],
            stream=False
        )
        
        raw = response.choices[0].message.content.strip()
        '''
        raw = """
        ```json
        {
            "input_specifications": [
                {
                    "type": "int",
                    "low": 0,
                    "high": 100
                },
                {
                    "type": "int",
                    "low": 0,
                    "high": 100
                },
                {
                    "type": "int",
                    "low": 0,
                    "high": 100
                }
            ]
        }
        ```
        """'
        '''

        json_string = re.search(r'```json\n(.*?)```', raw, re.DOTALL).group(1)
        model_output = json.loads(json_string)

        test_cases = generate_test_cases(model_output, NUM_TEST_CASES, NUM_BATCHES, problem_editorial)

        print(test_cases)

        result = input("Is this ok? Type 'yes' to generate test files: ").strip()

        if result == "yes":
            create_test_files(test_cases, problem_id)

            print("Test files generated successfully")
        else:
            print("Test generation cancelled")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
