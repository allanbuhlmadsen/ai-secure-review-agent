from pathlib import Path


HTTP_ATTRIBUTES = [
    "[HttpGet",
    "[HttpPost",
    "[HttpPut",
    "[HttpPatch",
    "[HttpDelete"
]


def scan_for_missing_authorization(file_path: Path) -> list[dict]:
    findings: list[dict] = []

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    has_controller_authorize = any("[Authorize" in line for line in lines)

    for line_number, line in enumerate(lines, start=1):
        is_endpoint = any(attribute in line for attribute in HTTP_ATTRIBUTES)

        if is_endpoint and not has_controller_authorize:
            findings.append({
                "type": "Missing Authorization",
                "file": str(file_path),
                "line": line_number,
                "code": line.strip()
            })

    return findings