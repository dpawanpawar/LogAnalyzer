import re
from collections import defaultdict

# Function to read the log file
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Function to extract errors from log lines
def extract_errors(log_lines):
    error_pattern = re.compile(r"ERROR|Error|error|WARNING|Warning|warning")
    errors = [line for line in log_lines if error_pattern.search(line)]
    return errors

# Function to categorize and count errors
def categorize_errors(errors):
    error_dict = defaultdict(int)
    error_type_pattern = re.compile(r"(ERROR|WARNING|Error|Warning|error|warning)")
    
    for error in errors:
        match = error_type_pattern.search(error)
        if match:
            error_type = match.group(1)
            error_dict[error_type] += 1
    
    return error_dict

# Function to generate a report
def generate_report(error_dict):
    report = "Error Report:\n"
    for error_type, count in error_dict.items():
        report += f"{error_type}: {count}\n"
    return report

# Main function
def analyze_log(file_path):
    log_lines = read_log_file(file_path)
    errors = extract_errors(log_lines)
    error_dict = categorize_errors(errors)
    report = generate_report(error_dict)
    return report

# Example usage
file_path = 'Windows_2k.log'
report = analyze_log(file_path)
print(report)
