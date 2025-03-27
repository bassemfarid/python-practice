import subprocess
import os
import sys

# Function to run the existing script and capture its output
def run_existing_script(input_values, script_path):
    # Construct the command to run the existing script
    command = ["python3", script_path]
    
    # Open the process using subprocess.Popen
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Send the input values to stdin (one per line as the script expects)
    input_data = "\n".join(input_values) + "\n"
    stdout, stderr = process.communicate(input=input_data)  # Wait for the process to finish and get output

    # Return the output (stdout) and any errors (stderr)
    if stderr:
        return stderr.strip()
    return stdout.strip()

# Function to write input and output to files
def write_to_files(base_dir, batch_number, test_case_number, input_values, output):
    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Format the test case number with leading zeros
    test_case_filename = f"{test_case_number:02d}"

    # Define file names for input and output
    input_file = os.path.join(base_dir, f"{batch_number}-{test_case_filename}.in")
    output_file = os.path.join(base_dir, f"{batch_number}-{test_case_filename}.out")
    
    # Write input values to the .in file
    with open(input_file, 'w') as f:
        f.write("\n".join(input_values) + "\n")

    # Write output to the .out file
    with open(output_file, 'w') as f:
        f.write(output + "\n")

# Main function to run the test cases
def generate_test_cases(base_dir, input_batches, script_path):
    # Start batch numbering from 1
    batch_number = 1

    # Loop through each batch in input_batches
    for batch in input_batches:
        # Loop through each test case in the current batch
        test_case_number = 1
        for input_values in batch:
            # Run the script with the dynamic input values
            output = run_existing_script(input_values, script_path)
            
            # Write the input and output to the files
            write_to_files(base_dir, batch_number, test_case_number, input_values, output)
            
            # Increment test case number for the next test case
            test_case_number += 1
        
        # Increment batch number for the next batch
        batch_number += 1

# Example 3D input batches (each sublist is a batch, containing test cases, which contain input values)
input_batches = [
    # Batch 1
    [
        ["20"],                
        ["10495"],
        ["304.45"],
        ["40593"],
        ["18249.1204"]
    ],
    # Batch 2, student average lower than 80
    [
        ["-120"],
        ["-45"],
        ["-4950.4193"],
        ["-79.999"],
        ["-59.00001"]
    ]
]

# User-defined base directory for storing test case files
base_dir = "/Users/qianjunye/Documents/GitHub/python-practice/tests/02-01-04"  # You can change this path to any location you prefer
script_path = "/Users/qianjunye/Documents/GitHub/python-practice/Unit-02/Chapter-01/02-01-04.py"
# Generate the test cases and store them in the specified location
generate_test_cases(base_dir, input_batches, script_path)

# Print confirmation message
print(f"Test cases have been successfully generated and saved in {base_dir}.")

# Exit the script
sys.exit()