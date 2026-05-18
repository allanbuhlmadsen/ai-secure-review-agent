from pathlib import Path


HTTP_ATTRIBUTES = [
    "[HttpGet",
    "[HttpPost",
    "[HttpPut",
    "[HttpPatch",
    "[HttpDelete"
]


VALIDATION_INDICATORS = [
    "ModelState.IsValid",
    "[Required]",
    "[StringLength]",
    "[Range]",
    "[RegularExpression]",
    "IValidatableObject",
    "Validator"
]


def scan_for_missing_input_validation(file_path: Path) -> list[dict]:
    findings: list[dict] = []

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    has_validation = any(indicator in content for indicator in VALIDATION_INDICATORS)

    for line_number, line in enumerate(lines, start=1):
        is_endpoint = any(attribute in line for attribute in HTTP_ATTRIBUTES)

        if is_endpoint and not has_validation:
            findings.append({
                "type": "Missing Input Validation",
                "file": str(file_path),
                "line": line_number,
                "code": line.strip()
            })

    return findings