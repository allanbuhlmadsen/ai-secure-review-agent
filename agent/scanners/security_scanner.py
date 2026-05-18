from pathlib import Path

from scanners.hardcoded_secret_scanner import scan_for_hardcoded_secrets
from scanners.sql_injection_scanner import scan_for_sql_injection
from scanners.authorization_scanner import scan_for_missing_authorization
from scanners.input_validation_scanner import scan_for_missing_input_validation

from tools.tool_logger import log_tool_call


def run_all_scanners(files: list[Path]) -> list[dict]:
    all_findings = []

    for file in files:
        secret_findings = scan_for_hardcoded_secrets(file)
        log_tool_call("hardcoded_secret_scanner", file, len(secret_findings))

        sql_findings = scan_for_sql_injection(file)
        log_tool_call("sql_injection_scanner", file, len(sql_findings))

        authorization_findings = scan_for_missing_authorization(file)
        log_tool_call("authorization_scanner", file, len(authorization_findings))

        validation_findings = scan_for_missing_input_validation(file)
        log_tool_call("input_validation_scanner", file, len(validation_findings))

        all_findings.extend(secret_findings)
        all_findings.extend(sql_findings)
        all_findings.extend(authorization_findings)
        all_findings.extend(validation_findings)

    return all_findings