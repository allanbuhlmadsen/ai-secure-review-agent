from pathlib import Path


ALLOWED_EXTENSIONS = {".cs", ".json", ".config"}


def find_relevant_files(repository_path: str) -> list[Path]:
    root_path = Path(repository_path)

    if not root_path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repository_path}")

    relevant_files: list[Path] = []

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in ALLOWED_EXTENSIONS:
            relevant_files.append(file_path)

    return relevant_files