from pathlib import Path
from datetime import datetime
import json


TOOL_CALLS = []


def log_tool_call(tool_name: str, file_path: Path, findings_count: int) -> None:
    TOOL_CALLS.append({
        "timestamp": datetime.utcnow().isoformat(),
        "tool": tool_name,
        "file": str(file_path),
        "findings_count": findings_count
    })


def write_tool_call_log(file_name: str = "tool_call_log.json") -> None:
    output_directory = Path("outputs")
    output_directory.mkdir(exist_ok=True)

    output_file = output_directory / file_name

    output_file.write_text(
        json.dumps(TOOL_CALLS, indent=2),
        encoding="utf-8"
    )

    print(f"Tool call log written to: {output_file}")