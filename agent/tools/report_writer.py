from pathlib import Path


OUTPUT_DIRECTORY = Path("outputs")


def write_security_report(report_content: str, file_name: str = "security_report.json") -> None:
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)

    output_file = OUTPUT_DIRECTORY / file_name

    output_file.write_text(report_content, encoding="utf-8")

    print(f"\nSecurity report written to: {output_file}")