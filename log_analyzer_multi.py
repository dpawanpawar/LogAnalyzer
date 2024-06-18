import os
import re
import json
from collections import defaultdict

# Function to read a single log file
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Function to extract errors from log lines
def extract_errors(log_lines):
    error_pattern = re.compile(r"ERROR|Error|error|Failed") #|WARNING|Warning|warning")
    errors = [line for line in log_lines if error_pattern.search(line)]
    return errors

# Function to categorize and count errors
def categorize_errors(errors):
    error_dict = defaultdict(lambda: {"count": 0, "descriptions": []})
    error_type_pattern = re.compile(r"(ERROR|Error|error|Failed)") #|WARNING|Warning|warning)")
    
    for error in errors:
        match = error_type_pattern.search(error)
        if match:
            error_type = match.group(1)
            error_dict[error_type]["count"] += 1
            error_dict[error_type]["descriptions"].append(error.strip())
    
    return error_dict

# Function to generate a report
def generate_report(error_dict, title):
    report = f"Error Report for {title}:\n"
    for error_type, details in error_dict.items():
        report += f"{error_type}: {details['count']}\n"
        for desc in details["descriptions"]:
            report += f"  - {desc}\n"
    return report

# Function to analyze a single log file
def analyze_log(file_path):
    log_lines = read_log_file(file_path)
    errors = extract_errors(log_lines)
    error_dict = categorize_errors(errors)
    report = generate_report(error_dict, os.path.basename(file_path))
    return error_dict, report

# Function to analyze all log files in multiple directories
def analyze_logs_in_folders(folder_paths):
    overview_dict = defaultdict(lambda: defaultdict(lambda: {"count": 0, "descriptions": []}))
    detailed_reports = []

    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                error_dict, report = analyze_log(file_path)
                detailed_reports.append(report)
                for error_type, details in error_dict.items():
                    overview_dict[file_name][error_type]["count"] += details["count"]
                    overview_dict[file_name][error_type]["descriptions"].extend(details["descriptions"])

    overview_report = generate_report(overview_dict, "Overview")
    return overview_dict, overview_report, detailed_reports

# Function to save the overview report as JSON
def save_overview_as_json(overview_dict, output_file):
    with open(output_file, 'w') as file:
        json.dump(overview_dict, file, indent=4)

# Main function to run the analysis
def main():
    folder_paths = [
        r'C:\Users\dpawa\Desktop\Python_basic\LogAnalyzer\logs',  # Replace with the path to your first log folder
        r'C:\Users\dpawa\Desktop\Python_basic\Logfiles',  # Replace with the path to your second log folder
        # Add more paths as needed
    ]
    overview_dict, overview_report, detailed_reports = analyze_logs_in_folders(folder_paths)
    
    # Print overview report
    print(overview_report)
    
    # Print detailed reports
    for report in detailed_reports:
        print(report)

    # Save overview report as JSON
    json_output_file = 'overview_report.json'  # Specify the output JSON file path
    save_overview_as_json(overview_dict, json_output_file)
    print(f"Overview report saved as {json_output_file}")

# Run the main function
if __name__ == "__main__":
    main()

