import re
from pathlib import Path


SQL_INJECTION_PATTERNS = [
    r"SELECT\s+.*\+\s*\w+",
    r"INSERT\s+.*\+\s*\w+",
    r"UPDATE\s+.*\+\s*\w+",
    r"DELETE\s+.*\+\s*\w+"
]


def scan_for_sql_injection(file_path: Path) -> list[dict]:
    findings: list[dict] = []

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    for line_number, line in enumerate(content.splitlines(), start=1):
        for pattern in SQL_INJECTION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "type": "Potential SQL Injection",
                    "file": str(file_path),
                    "line": line_number,
                    "code": line.strip()
                })

    return findings