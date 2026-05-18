# AI Secure Coding Review Agent

AI Secure Coding Review Agent is a bounded AI agentic system designed to analyze small C#/.NET repositories for common secure coding issues using deterministic scanning tools combined with LLM-based reasoning.

The project was developed as part of a Machine Learning and Artificial Intelligence course focused on:
- LLMs
- AI agents
- tool-calling
- grounded reasoning
- hallucination mitigation
- structured outputs
- evaluation of agent behavior

The system uses deterministic scanners to identify potential security findings and then uses an LLM to:
- explain vulnerabilities
- assign severity levels
- recommend mitigations
- return structured JSON output

The project intentionally focuses on small-scale repository analysis and explainable AI-agent workflows rather than advanced static analysis.

---

# Features

- Repository traversal for C#/.NET repositories
- Deterministic regex-based security scanning
- LLM-based security reasoning using Mistral AI
- Structured JSON output
- Tool call logging
- Deterministic JSON validation
- Hallucination mitigation through grounded prompting
- Evaluation using fixed test repositories and test cases

---

# Supported Security Findings

Version 1 supports detection and analysis of:
- Hardcoded Secrets
- Potential SQL Injection
- Missing Authorization
- Missing Input Validation

---

# System Architecture

The system is structured as a layered AI-agent workflow consisting of:
1. Repository traversal
2. Deterministic security scanning
3. Tool call logging
4. LLM-based reasoning
5. JSON validation
6. Structured report generation

The deterministic scanner layer is responsible for grounded factual findings, while the LLM layer is responsible for explanation, severity assessment, and mitigation recommendations.

The architecture intentionally separates:
- deterministic analysis
- probabilistic reasoning
- output validation

to reduce hallucination risk and improve traceability.

---

# Project Structure

```text
ai-secure-review-agent/
├── agent/
│   ├── main.py
│   ├── config.py
│   ├── scanners/
│   │   ├── repository_scanner.py
│   │   ├── hardcoded_secret_scanner.py
│   │   ├── sql_injection_scanner.py
│   │   ├── authorization_scanner.py
│   │   ├── input_validation_scanner.py
│   │   └── security_scanner.py
│   ├── tools/
│   │   ├── llm_security_analyzer.py
│   │   ├── tool_logger.py
│   │   ├── json_validator.py
│   │   └── report_writer.py
│   ├── evaluation/
│   │   └── evaluation_cases.md
│   └── outputs/
│       ├── security_report.json
│       └── tool_call_log.json
├── test_repositories/
├── README.md
├── requirements.txt
└── .env
``` 

---

# Agent Workflow

The agent executes the following workflow:

1. Traverse the repository and identify relevant files
2. Execute deterministic security scanners
3. Log all tool calls and findings count
4. Send scanner findings to the LLM
5. Generate grounded security analysis
6. Validate JSON output deterministically
7. Write structured security report
8. Write tool call log

The workflow combines deterministic tooling with LLM-based reasoning while enforcing validation and traceability.

---

# Architecture Flow

```text
Repository
    │
    ▼
Repository Scanner
    │
    ▼
Deterministic Security Scanners
    │
    ├── Hardcoded Secret Scanner
    ├── SQL Injection Scanner
    ├── Authorization Scanner
    └── Input Validation Scanner
    │
    ▼
Tool Call Logger
    │
    ▼
LLM Security Analyzer (Mistral)
    │
    ▼
JSON Validator
    │
    ▼
Structured Security Report
    │
    ├── security_report.json
    └── tool_call_log.json
```

---

# Deterministic Validation

The project includes deterministic validation steps to improve robustness and reduce unreliable LLM output.

Implemented validation mechanisms:
- deterministic regex-based scanner findings
- JSON validation of LLM responses

Before a security report is written, the system validates that the LLM response is valid JSON.

If invalid JSON is detected:
- the security report is not written
- an error message is shown
- the tool call log is still preserved

This improves:
- reliability
- failure handling
- output consistency

---

# Dependencies

Main dependencies used in the project:

```text
autogen==0.3.1
mistralai==1.2.3
python-dotenv==1.2.2

Recommended Python version:
- Python 3.11+
```

Additional Python standard library modules:
- json
- pathlib
- os
- re
- sys
- datetime

---

# Environment Variables

The project requires a `.env` file containing a valid Mistral API key.

Example:

```text
MISTRAL_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd ai-secure-review-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Some AutoGen installations may require temporarily disabling Git clone protection on Windows PowerShell:

```powershell
$env:GIT_CLONE_PROTECTION_ACTIVE="false"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Agent

Navigate to the `agent` directory and run the agent using a repository path as argument.

Example:

```bash
python main.py ../test_repositories/vulnerable_api
```

Example repositories:
- vulnerable_api
- safe_api
- secret_only_api
- duplicate_secret_api
- false_positive_api
- sql_false_negative_api
- minimal_safe_api
- empty_repository

---

# Output Files

The system generates:

## Security Report

```text
outputs/security_report.json
```

Contains:
- vulnerability findings
- severity levels
- explanations
- mitigation recommendations

## Tool Call Log

```text
outputs/tool_call_log.json
```

Contains:
- tool calls
- analyzed files
- timestamps
- findings count

---

# Example Output

Example security report:

```json
[
  {
    "vulnerability_type": "Hardcoded Secret",
    "file": "../test_repositories/secret_only_api/SecretController.cs",
    "lines": [20],
    "severity": "High",
    "explanation": "The API key is hardcoded into the source code, which poses a significant security risk if the code is exposed.",
    "recommendation": "Remove the hardcoded API key and use a secure method to manage and retrieve it, such as environment variables or a secure secret management system."
  }
]
```

Example tool call log:

```json
[
  {
    "timestamp": "2026-05-15T10:44:17.540545",
    "tool": "hardcoded_secret_scanner",
    "file": "../test_repositories/secret_only_api/SecretController.cs",
    "findings_count": 1
  }
]
```

---

# Evaluation

The project was evaluated using fixed repositories and predefined test cases.

The evaluation included:
- positive detections
- no-findings repositories
- hallucination control
- false positives
- false negatives
- deduplication behaviour
- invalid repository paths
- empty repositories
- malformed LLM output

Evaluation cases are documented in:

```text
agent/evaluation/evaluation_cases.md
```

---

# Failure Handling

The project includes basic failure handling mechanisms for:
- invalid repository paths
- malformed LLM JSON responses
- empty repositories

The system is designed to fail gracefully while preserving:
- tool call logs
- deterministic validation behaviour
- output consistency

---

# Limitations

The project intentionally uses simple regex-based scanning and therefore has several limitations.

Known limitations include:
- false positives
- false negatives
- lack of AST parsing
- no compiler-level analysis
- no dataflow analysis
- no dependency vulnerability scanning
- no multi-language support
- LLM output variability between runs

The system is intended as a bounded educational AI-agent project rather than a production-grade security scanner.

---

# Academic Focus

The project focuses on:
- AI agents
- tool-calling
- grounded LLM reasoning
- hallucination mitigation
- structured outputs
- deterministic validation
- explainable AI-agent workflows

The project does not focus on:
- advanced machine learning models
- training custom models
- enterprise static analysis
- advanced compiler analysis
- large-scale repository analysis

---

# License

Educational project developed for a Machine Learning and Artificial Intelligence course.
