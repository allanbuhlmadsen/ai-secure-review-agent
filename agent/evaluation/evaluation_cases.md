# Evaluation Cases

| Case ID | Repository | Scenario | Expected Scanner Findings | Expected AI Behaviour | Result |
|---|---|---|---|---|---|
| E01 | vulnerable_api | Repository contains hardcoded database credentials | Hardcoded Secret | Explain risk and recommend secret management | Passed |
| E02 | vulnerable_api | Repository contains SQL query built with string concatenation | Potential SQL Injection | Explain SQL injection risk and recommend parameterized queries | Passed |
| E03 | vulnerable_api | Endpoint has no authorization attribute | Missing Authorization | Explain unauthorized access risk | Passed |
| E04 | vulnerable_api | Endpoint has no visible input validation | Missing Input Validation | Explain validation risk | Passed |
| E05 | safe_api | Repository uses configuration-based connection string, parameterized SQL, authorization and validation | No findings | Return empty JSON array without hallucinating | Passed |
| E06 | secret_only_api | Repository contains only a hardcoded API key | Hardcoded Secret | Return only one finding and avoid hallucinating unrelated vulnerabilities | Passed |
| E07 | minimal_safe_api | Minimal controller with authorization and no endpoints | No findings | Return empty JSON array without hallucinating | Passed |
| E08 | duplicate_secret_api | Repository contains two hardcoded API keys in the same controller | 2 x Hardcoded Secret | Combine related findings into one structured result | Passed |
| E09 | false_positive_api | Repository contains a demo token-like value | Hardcoded Secret | Analyze finding without inventing additional vulnerabilities | Passed with limitation |
| E10 | sql_false_negative_api | Repository contains SQL query built with string interpolation | No findings | Return empty JSON because LLM only receives scanner findings | Failed as detection / Passed as hallucination control |

---

# Actual Results

## E01 – Hardcoded Secret

Repository:
`vulnerable_api`

Deterministic scanner finding:

{
  "type": "Hardcoded Secret",
  "file": "..\\test_repositories\\vulnerable_api\\UserController.cs",
  "line": 11
}

LLM analysis result:
- Severity: High
- Correctly identified hardcoded credentials
- Recommended secure secret management

Result:
Passed

---

## E02 – Potential SQL Injection

Repository:
`vulnerable_api`

Deterministic scanner finding:

{
  "type": "Potential SQL Injection",
  "file": "..\\test_repositories\\vulnerable_api\\UserController.cs",
  "line": 17
}

LLM analysis result:
- Severity: High
- Correctly identified string concatenation with user input
- Recommended parameterized queries

Result:
Passed

---

## E03 – Missing Authorization

Repository:
`vulnerable_api`

Deterministic scanner finding:

{
  "type": "Missing Authorization",
  "file": "..\\test_repositories\\vulnerable_api\\UserController.cs",
  "line": 13
}

LLM analysis result:
- Severity: Medium
- Correctly identified missing authorization protection
- Recommended implementing authorization checks

Result:
Passed

---

## E04 – Missing Input Validation

Repository:
`vulnerable_api`

Deterministic scanner finding:

{
  "type": "Missing Input Validation",
  "file": "..\\test_repositories\\vulnerable_api\\UserController.cs",
  "line": 13
}

LLM analysis result:
- Severity: Medium
- Correctly identified lack of visible validation
- Recommended input validation

Result:
Passed

---

## E05 – Safe Repository

Repository:
`safe_api`

Deterministic scanner findings:

[]

LLM analysis result:

[]

Result:
Passed

Notes:
- Initial hardcoded secret regex caused a false positive on:
  `configuration.GetConnectionString("DefaultConnection")`
- Regex rule was refined to reduce false positives.
- After refinement, the repository produced no findings.

---

## E06 – Secret Only Repository

Repository:
`secret_only_api`

Deterministic scanner finding:

{
  "type": "Hardcoded Secret",
  "file": "..\\test_repositories\\secret_only_api\\SecretController.cs",
  "line": 20,
  "code": "private const string ApiKey = \"my-secret-api-key-123\";"
}

LLM analysis result:
- Severity: High
- Correctly identified the hardcoded API key
- Recommended environment variables or secure secret management
- Did not invent SQL injection, authorization, or validation findings

Result:
Passed

---

## E07 – Minimal Safe Repository

Repository:
`minimal_safe_api`

Deterministic scanner findings:

[]

LLM analysis result:

[]

Result:
Passed

Notes:
- The repository contains no HTTP endpoint methods.
- The scanner correctly produced no findings.
- The LLM correctly returned an empty JSON array.
- No vulnerabilities were hallucinated.

---

## E08 – Duplicate Secret Repository

Repository:
`duplicate_secret_api`

Deterministic scanner findings:

[
  {
    "type": "Hardcoded Secret",
    "file": "..\\test_repositories\\duplicate_secret_api\\DuplicateSecretController.cs",
    "line": 19,
    "code": "private const string ApiKey = \"duplicate-secret-api-key-123\";"
  },
  {
    "type": "Hardcoded Secret",
    "file": "..\\test_repositories\\duplicate_secret_api\\DuplicateSecretController.cs",
    "line": 20,
    "code": "private const string BackupApiKey = \"duplicate-backup-api-key-456\";"
  }
]

LLM analysis result:
- Severity: High
- Combined both hardcoded API keys into one structured finding
- Included both line numbers: 19 and 20
- Recommended secure secret management
- Did not invent unrelated vulnerabilities

Result:
Passed

---

## E09 – False Positive Repository

Repository:
`false_positive_api`

Deterministic scanner finding:

{
  "type": "Hardcoded Secret",
  "file": "..\\test_repositories\\false_positive_api\\FalsePositiveController.cs",
  "line": 19,
  "code": "private const string Token = \"demo-value-used-for-testing-only\";"
}

LLM analysis result:
- Severity: Medium
- Correctly analyzed the scanner finding
- Did not invent unrelated vulnerabilities
- Treated the token-like value as a potential secret

Result:
Passed with limitation

Notes:
- This case demonstrates a potential false positive.
- The scanner matched the variable because it used the keyword "Token".
- The value was intentionally a harmless demo string.
- The system lacks deeper semantic understanding of whether the value is actually sensitive.
- This demonstrates a limitation of regex-based deterministic scanning.

---

## E10 – SQL False Negative Repository

Repository:
`sql_false_negative_api`

Deterministic scanner findings:

[]

LLM analysis result:

[]

Result:
Failed as detection / Passed as hallucination control

Notes:
- This case contains a SQL query built with C# string interpolation.
- The current SQL injection scanner only detects string concatenation using `+`.
- Therefore, the scanner missed this vulnerability pattern.
- The LLM returned an empty JSON array because it was only allowed to analyze provided scanner findings.
- This demonstrates a false negative caused by limited regex coverage.
- At the same time, it demonstrates hallucination control because the LLM did not invent findings that were not provided by the scanner.

---

# Evaluation Summary

The evaluation demonstrated that the AI Secure Coding Review Agent was able to detect multiple common secure coding issues in small C#/.NET repositories using deterministic scanning tools combined with LLM-based reasoning.

The deterministic scanner layer successfully detected:
- hardcoded secrets
- SQL injection through string concatenation
- missing authorization
- missing input validation

The LLM layer successfully:
- explained detected vulnerabilities
- assigned severity levels
- generated mitigation recommendations
- returned structured JSON output
- avoided hallucinating vulnerabilities in repositories without scanner findings
- combined related findings into consolidated results

The evaluation also demonstrated important limitations.

False positives occurred because the regex-based scanners relied on simple keyword matching without deeper semantic understanding. For example, a harmless demo token value was interpreted as a potential secret.

False negatives also occurred. A SQL query using C# string interpolation was not detected because the scanner only searched for string concatenation patterns using the `+` operator.

The evaluation therefore demonstrated both the strengths and limitations of combining deterministic scanning with LLM-based reasoning.

The project showed that:
- deterministic tools can provide grounded factual findings
- LLMs can provide explanation and reasoning on top of deterministic findings
- hallucination risk can be reduced by restricting the LLM to scanner-provided findings
- structured JSON output improves consistency and evaluability

At the same time, the project also showed that simple regex-based scanning cannot replace advanced static analysis techniques such as AST parsing, compiler analysis, or dataflow analysis.


---

# Failure Handling Evaluation

## F01 – Invalid Repository Path

Input:

../test_repositories/does_not_exist

Result:

Error: Repository path does not exist: ../test_repositories/does_not_exist

Assessment:
Passed

Notes:
- The agent handled an invalid repository path without crashing.
- No stack trace was shown to the user.
- The program exited gracefully with exit code 0.

---

## F02 – Empty Repository

Input:

../test_repositories/empty_repository

Result:

Deterministic scanner findings:

AI security analysis:
[]

Assessment:
Passed

Notes:
- The agent handled an empty repository without crashing.
- No scanner findings were produced.
- The LLM returned an empty JSON array.
- The report writer and tool call logger still executed successfully.

---

## F03 – Invalid LLM JSON Response

Input:

../test_repositories/secret_only_api

Simulated LLM response:

INVALID JSON RESPONSE

Result:

Error: LLM response was not valid JSON.
Tool call log written to: outputs\tool_call_log.json

Assessment:
Passed

Notes:
- The agent validates the LLM response before writing the security report.
- Invalid JSON output is detected deterministically.
- The security report is not written when the LLM response is invalid.
- The tool call log is still written, preserving traceability.
- This demonstrates failure handling for malformed LLM output.