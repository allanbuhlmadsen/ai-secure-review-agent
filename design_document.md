# AI Secure Coding Review Agent – Designdokument

## 1. Introduktion

AI Secure Coding Review Agent er et afgrænset AI-agent-system, der analyserer mindre C#/.NET-repositories for almindelige secure coding-problemer. Systemet kombinerer deterministiske scanning tools med LLM-baseret analyse og forklaring.

Projektet er udviklet til et Machine Learning-fag, der bl.a. har haft fokus på moderne AI-systemer, herunder:
- LLMs
- AI-agenter
- tool-calling
- grounded reasoning
- hallucination mitigation
- structured outputs
- evaluering af agentadfærd

Formålet er ikke at bygge en fuld static analysis engine eller en produktionsklar security scanner. Formålet er i stedet at demonstrere, hvordan en AI-agent kan bruge konkrete tools til at finde faktuelle kodefund og derefter bruge en LLM til at forklare risiko, severity-vurdering og mulige mitigation-forslag.

Systemet analyserer i version 1 fire typer secure coding-problemer:
- Hardcoded Secrets
- Potential SQL Injection
- Missing Authorization
- Missing Input Validation

Designet adskiller bevidst:
- deterministisk scanning
- LLM-baseret reasoning
- deterministisk validering af output

Denne opdeling gør agentens workflow mere gennemsigtigt, reducerer risikoen for hallucinationer og gør outputtet lettere at evaluere.

## 2. Systemarkitektur

Systemet er opbygget som et lagdelt AI-agent-workflow, hvor deterministiske tools og LLM-baseret reasoning arbejder sammen i separate trin.

Workflowet består overordnet af følgende faser:

1. Repository traversal
2. Deterministisk scanning
3. Tool call logging
4. LLM-baseret analyse
5. JSON-validering
6. Rapportgenerering

Først gennemgår systemet et repository og identificerer relevante filer, eksempelvis `.cs`-filer. Derefter udføres flere deterministiske sikkerhedsscannere, som søger efter konkrete mønstre ved hjælp af regulære udtryk (regex) og keyword-baseret scanning.

De deterministiske scannere fungerer som systemets grounded data layer. Det betyder, at LLM’en ikke selv gennemgår hele repository’et, men i stedet modtager allerede identificerede scannerfund som input.

Efter scanning sendes fundene til LLM-laget, som anvender Mistral AI til at:
- forklare sårbarheder
- udføre severity-vurderinger
- foreslå mitigation-forslag
- kombinere relaterede fund
- returnere structured JSON output

Systemet logger samtidig alle tool calls med:
- tool-navn
- filnavn
- timestamp
- antal fund

Dette forbedrer systemets transparens og gør agentens adfærd lettere at analysere og evaluere.

Før output gemmes, udføres en deterministisk JSON-validering. Hvis LLM’en returnerer ugyldigt JSON, bliver rapporten ikke skrevet. Dette fungerer som en simpel guardrail mod ukorrekt eller ustabilt output.

Arkitekturen er bevidst designet med tydelig adskillelse mellem:
- deterministiske tools
- probabilistisk LLM-reasoning
- outputvalidering

Denne opdeling reducerer hallucinationsrisiko og gør systemets beslutningsflow mere forklarligt.

## 3. Deterministiske Tools

Systemet anvender flere deterministiske værktøjer til repository traversal, scanning, logging og validering. Disse tools fungerer som agentens faktuelle og verificerbare datalag.

### Repository Scanner

`repository_scanner.py` gennemgår repository-strukturen og identificerer relevante filer baseret på filendelser som:
- `.cs`
- `.json`
- `.config`

Dette begrænser analysen til relevante filer og reducerer støj i workflowet.

### Sikkerhedsscannere

Systemet anvender fire specialiserede sikkerhedsscannere:

- `hardcoded_secret_scanner.py`
- `sql_injection_scanner.py`
- `authorization_scanner.py`
- `input_validation_scanner.py`

Scannerne anvender primært regex- og keyword-baseret scanning til at identificere potentielle secure coding-problemer.

Eksempler:
- hardcoded passwords eller API keys
- SQL queries bygget via string concatenation
- endpoints uden `[Authorize]`
- endpoints uden synlig inputvalidering

Scanningen er bevidst simpel og afgrænset. Projektet fokuserer på AI-agent workflows og tool orchestration fremfor avanceret static analysis.

### Tool Logger

`tool_logger.py` registrerer:
- hvilke tools der blev kaldt
- hvilke filer der blev analyseret
- timestamps
- antal fund

Loggen gemmes som structured JSON og forbedrer systemets sporbarhed og transparens.

### JSON Validator

`json_validator.py` fungerer som en deterministisk guardrail.

Efter LLM-analysen valideres outputtet med standard JSON parsing. Hvis output ikke er valid JSON:
- stoppes rapportskrivningen
- brugeren får en fejlmeddelelse
- tool call loggen bevares

Dette reducerer risikoen for ustabilt eller ubrugeligt LLM-output.

## 4. LLM-baseret Analyse og Prompting

Efter den deterministiske scanning sendes scannerfundene til LLM-laget, som anvender Mistral AI til at analysere fundene og generere strukturerede sikkerhedsvurderinger.

LLM’en anvendes ikke til selvstændigt at scanne repository’et. I stedet modtager den allerede identificerede fund fra de deterministiske tools. Dette designvalg reducerer hallucinationsrisiko og gør outputtet mere grounded og verificerbart.

LLM’en instrueres eksplicit gennem prompten til:
- kun at anvende de fund, der sendes som input
- ikke at opfinde filer, linjenumre eller vulnerabilities
- kombinere relaterede fund
- returnere valid JSON
- undgå forklarende tekst udenfor JSON-outputtet

Prompten specificerer samtidig den ønskede struktur for hvert fund:
- vulnerability_type
- file
- lines
- severity
- explanation
- recommendation

Severity-vurderingerne genereres af LLM’en og er derfor probabilistiske vurderinger fremfor objektivt verificerede sikkerhedsvurderinger.

Systemet bruger structured JSON output for at gøre resultaterne:
- maskinlæsbare
- evaluerbare
- sammenlignelige mellem testcases

Denne tilgang gør det muligt at kombinere deterministiske tools med fleksibel LLM-baseret reasoning uden at give LLM’en fuld kontrol over analysegrundlaget.

## 5. Hallucination Mitigation og Failure Handling

En central udfordring ved LLM-baserede systemer er risikoen for hallucinationer, hvor modellen genererer information, som ikke er baseret på faktiske data.

Projektet forsøger at reducere denne risiko gennem flere designvalg.

### Grounded Scanner Findings

LLM’en modtager ikke hele repository’et som input. Den modtager kun konkrete scannerfund fra de deterministiske tools.

Dette begrænser analysegrundlaget til verificerbare fund og reducerer sandsynligheden for, at modellen opfinder nye vulnerabilities eller kodefund.

### Restriktiv Prompting

Prompten instruerer eksplicit LLM’en til:
- kun at analysere eksisterende scannerfund
- ikke at opfinde filer eller linjenumre
- returnere ren JSON uden ekstra tekst

Dette fungerer som en simpel prompt-baseret guardrail.

### Deterministisk JSON-validering

Efter LLM-analysen udfører systemet en deterministisk validering af outputtet.

Hvis output ikke er valid JSON:
- stoppes rapportskrivningen
- brugeren modtager en fejlmeddelelse
- tool call loggen bevares

Dette reducerer risikoen for ustabilt eller ubrugeligt output.

### Failure Handling

Projektet indeholder simple failure handling-mekanismer for:
- ugyldige repository paths
- tomme repositories
- malformed LLM JSON responses

Systemet er designet til at fejle kontrolleret fremfor at crashe ukontrolleret med stack traces.

### Kendte Begrænsninger

Selvom hallucinationsrisikoen reduceres, kan den ikke elimineres fuldstændigt.

Projektet har blandt andet følgende begrænsninger:
- regex-scanning kan give false positives
- regex-scanning kan give false negatives
- severity-vurderinger er LLM-baserede
- output kan variere mellem kørsler
- systemet udfører ikke AST parsing eller dataflow-analyse

Projektet demonstrerer derfor primært et kontrolleret AI-agent workflow fremfor perfekt sikkerhedsanalyse.

## 6. Evaluering

Systemet blev evalueret ved hjælp af faste testrepositories og prædefinerede testcases.

Evalueringen omfattede blandt andet:
- repositories med forventede vulnerabilities
- repositories uden fund
- false positives
- false negatives
- deduplikering af fund
- failure handling
- malformed LLM output

Projektet inkluderer blandt andet følgende typer testcases:
- repositories med hardcoded secrets
- repositories med SQL injection patterns
- sikre repositories uden findings
- repositories designet til at fremprovokere false positives
- repositories designet til at demonstrere false negatives
- tomme repositories
- ugyldige repository paths

Evalueringen viste, at systemet generelt producerede grounded og konsistente resultater indenfor det afgrænsede scope.

Et vigtigt resultat var identificeringen af en false positive i den første version af hardcoded secret-scanneren. Scanneren identificerede fejlagtigt en configuration-baseret connection string som en hardcoded secret. Regex-reglen blev efterfølgende forbedret for at reducere denne type fejl.

Projektet demonstrerede også, at:
- LLM’en kunne returnere tomt JSON-output uden hallucinerede fund
- relaterede findings kunne kombineres
- ugyldigt JSON-output kunne opdages deterministisk
- tool call logging fungerede korrekt gennem hele workflowet

Den samlede evaluering understøtter, at systemet fungerer som et kontrolleret AI-agent workflow med fokus på explainability og grounded reasoning.

---

## 7. Konklusion

Projektet demonstrerer, hvordan et moderne AI-agent-system kan kombinere deterministiske tools med LLM-baseret reasoning til secure coding-analyse.

Ved at adskille:
- scanning
- reasoning
- validering

opnår systemet et mere transparent og kontrolleret workflow end et rent LLM-baseret system.

Projektet viser samtidig både styrker og begrænsninger ved denne type AI-agentarkitektur. Deterministiske tools forbedrer grounding og reducerer hallucinationer, men simple regex-baserede scannere giver stadig risiko for false positives og false negatives.

Selvom systemet ikke er en produktionsklar security scanner, demonstrerer projektet centrale principper indenfor:
- AI agents
- tool-calling
- grounded reasoning
- hallucination mitigation
- structured outputs
- deterministic validation
- evaluering af agentadfærd

Projektet opfylder dermed formålet om at demonstrere et afgrænset, forklarligt og evaluerbart AI-agent-system.