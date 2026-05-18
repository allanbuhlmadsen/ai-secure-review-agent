import sys

from scanners.repository_scanner import find_relevant_files
from scanners.security_scanner import run_all_scanners

from tools.llm_security_analyzer import analyze_security_findings
from tools.report_writer import write_security_report
from tools.tool_logger import write_tool_call_log
from tools.json_validator import validate_json_output

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <repository_path>")
        return

    repository_path = sys.argv[1]

    try:
        files = find_relevant_files(repository_path)

    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    all_findings = run_all_scanners(files)

    print("Deterministic scanner findings:")

    for finding in all_findings:
        print(finding)

    print("\nAI security analysis:")

    analysis = analyze_security_findings(all_findings)

    if not validate_json_output(analysis):
        print("Error: LLM response was not valid JSON.")
        write_tool_call_log()
        return

    print(analysis)

    write_security_report(analysis)
    write_tool_call_log()


if __name__ == "__main__":
    main()