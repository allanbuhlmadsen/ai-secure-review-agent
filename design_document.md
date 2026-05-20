# AI Secure Coding Review Agent – Designdokument

## 1. Introduktion

AI Secure Coding Review Agent er et afgrænset AI-agent-system, der analyserer mindre C#/.NET-repositories for almindelige problemer inden for sikker kodning. Systemet kombinerer deterministiske værktøjer med LLM-baseret ræsonnement og analyse.

Projektet er udviklet til et Machine Learning-fag, der blandt andet har haft fokus på moderne AI-systemer, herunder:
- LLMs
- AI-agenter
- værktøjskald (tool-calling)
- grounded reasoning eller faktabaseret ræsonnement
- reduktion af hallucinationer (hallucination mitigation)
- strukturerede output (structured outputs)
- evaluering af agentadfærd

Formålet er ikke at bygge en fuld løsning til statisk analyse eller en produktionsklar sikkerhedsscanner. Formålet er i stedet at demonstrere, hvordan en AI-agent kan anvende konkrete værktøjer til at finde verificerbare kodefund og derefter anvende en LLM til at forklare risiko, lave alvorlighedsvurderinger og give forslag til håndtering deraf.

Systemet analyserer i version 1 fire typer problemer inden for sikker kodning:
- Hardkodede secrets
- SQL-injektioner
- Manglende autorisation
- Manglende input validering

Designet adskiller bevidst:
- deterministisk scanning
- LLM-baseret ræsonnement og analyse
- deterministisk validering af output

Denne opdeling gør agentens workflow mere gennemsigtigt, reducerer risikoen for hallucinationer og gør outputtet lettere at evaluere.

## 2. Systemarkitektur

Systemet er opbygget som et lagdelt AI-agent-system, hvor deterministiske værktøjer og LLM-baseret ræsonnement og analyse arbejder sammen i separate trin.

Systemets workflow består overordnet af følgende faser:

1. Gennemgang af repository
2. Deterministisk scanning
3. Logging af værktøjskald
4. LLM-baseret analyse
5. JSON-validering
6. Rapportgenerering

Først gennemgår systemet et repository og identificerer relevante filer, i dette tilfælde .cs-filer. Derefter udføres flere deterministiske sikkerhedsscan, som søger efter konkrete mønstre ved hjælp af regulære udtryk (regex) og keyword-baseret scanning.

De deterministiske scannere fungerer som systemets faktabaserede datalag, dvs. fundamentet for grounded reasoning. De sikrer, at LLM’en ikke selv gennemgår hele repository’et, men i stedet modtager allerede identificerede scannerfund som input.

Efter scanning sendes fundene til LLM-laget, som anvender Mistral AI til at:
- forklare sårbarheder
- udføre alvorlighedsvurderinger
- give anbefalinger til håndtering af hallucination
- kombinere relaterede fund
- returnere struktureret JSON-output

Systemet logger samtidig alle værktøjskald med:
- værktøjsnavn
- filnavn
- timestamp
- antal fund

Dette forbedrer systemets transparens og gør agentens adfærd lettere at analysere og evaluere.

Før output gemmes, udføres deterministisk JSON-validering. Hvis LLM’en returnerer ugyldigt JSON, bliver rapporten ikke skrevet. Dette fungerer som en simpel kontrolmekanisme mod ukorrekt eller ustabilt output.

Arkitekturen er bevidst designet med tydelig adskillelse mellem:
- deterministiske værktøjer
- sandsynlighedsbaseret ræsonnement og analyse med LLM
- outputvalidering

Denne opdeling reducerer hallucinationsrisiko og gør systemets workflow mere forklarligt.

## 3. Deterministiske værktøjer

Systemet anvender flere deterministiske værktøjer til gennemgang af repositories, scanning, logging og validering. Disse værktøjer fungerer som agentens faktabaserede datalag.

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

Scannerne anvender primært regex- og keyword-baseret scanning til at identificere potentielle problemer inden for sikker kodning.

Eksempler:
- hardkodede passwords eller API keys
- SQL queries bygget via string concatenation
- endpoints uden `[Authorize]`
- endpoints uden synlig inputvalidering

Scanningen er bevidst simpel og afgrænset. Projektet fokuserer på AI-agentens workflow og værktøjskoordinering (tool orchestration) fremfor avanceret statisk analyse.

### Tool Logger

`tool_logger.py` registrerer:
- hvilke værktøjer der blev kaldt
- hvilke filer der blev analyseret
- timestamps
- antal fund

Loggen gemmes som struktureret JSON-output og forbedrer systemets sporbarhed og transparens.

### JSON Validator

`json_validator.py` fungerer som en deterministisk kontrolmekanisme.

Efter LLM-analysen valideres outputtet med standard JSON parsing. Hvis output ikke er valid JSON:
- stoppes rapportskrivningen
- brugeren modtager en fejlmeddelelse
- loggen over værktøjskald bevares

Dette reducerer risikoen for ustabilt eller ubrugeligt LLM-output.

## 4. LLM-baseret Analyse og Prompting

Efter den deterministiske scanning sendes scannerfundene til LLM-laget, som anvender Mistral AI til at analysere fundene og generere strukturerede sikkerhedsvurderinger.

LLM’en anvendes ikke til selvstændigt at scanne repository’et. I stedet modtager den allerede identificerede fund fra de deterministiske værktøjer. Dette designvalg reducerer hallucinationsrisiko og gør outputtet faktabeseret (grounded) og derfor verificerbart.

LLM’en instrueres eksplicit gennem prompten til:
- kun at anvende de fund, der sendes som input
- ikke at opfinde filer, linjenumre eller sårbarheder
- kombinere relaterede fund
- returnere valid JSON
- undgå forklarende tekst udenfor JSON-outputtet

Prompten specificerer samtidig den ønskede struktur for hvert fund:
- sårbarhedstype (vulnerability_type)
- fil (file)
- linjer (lines)
- alvorlighed (severity)
- forklaring (explanation)
- anbefaling (recommendation)

Alvorlighedsvurderingerne genereres af LLM’en og er derfor sandsynlighedsbaserede vurderinger fremfor objektivt verificerede sikkerhedsvurderinger.

Systemet anvender struktureret JSON-output for at gøre resultaterne:
- maskinlæsbare
- evaluerbare
- sammenlignelige mellem testcases

Denne tilgang gør det muligt at kombinere deterministiske værktøjer med fleksibel LLM-baseret ræsonnement og analyse uden at give LLM’en fuld kontrol over analysegrundlaget.

## 5. Hallucinationsreduktion og Fejlhåndtering

En central udfordring ved LLM-baserede systemer er risikoen for hallucinationer, hvor modellen genererer information, som ikke er baseret på faktiske data.

Projektet forsøger at reducere denne risiko gennem flere designvalg.

### Faktabaserede verificerbare scannerfund

LLM’en modtager ikke hele repository’et som input. Den modtager kun konkrete scannerfund fra de deterministiske værktøjer.

Dette begrænser analysegrundlaget til verificerbare fund og reducerer sandsynligheden for, at modellen opfinder nye sårbarheder eller kodefund.

### Restriktiv Prompting

Prompten instruerer eksplicit LLM’en til:
- kun at analysere eksisterende scannerfund
- ikke at opfinde filer eller linjenumre
- returnere ren JSON uden ekstra tekst

Dette fungerer som en simpel prompt-baseret kontrolmekanisme.

### Deterministisk JSON-validering

Efter LLM-analysen udfører systemet en deterministisk validering af outputtet.

Hvis output ikke er valid JSON:
- stoppes rapportskrivningen
- brugeren modtager en fejlmeddelelse
- loggen over værktøjskald bevares

Dette reducerer risikoen for ustabilt eller ubrugeligt output.

### Fejlhåndtering

Projektet indeholder simple mekanismer til fejlhåndtering for:
- ugyldige repository paths
- tomme repositories
- ugyldigt JSON-output fra LLM’en

Systemet er designet til at fejle kontrolleret fremfor at crashe ukontrolleret med stack traces.

### Kendte Begrænsninger

Selvom hallucinationsrisikoen reduceres, kan den ikke elimineres fuldstændigt.

Projektet har blandt andet følgende begrænsninger:
- regex-baseret scanning kan give falske positiver
- regex-baseret scanning kan give falske negativer
- alvorlighedsvurderinger er LLM-baserede og dermed sandsynlighedsbaserede
- output kan variere mellem kørsler
- systemet udfører ikke AST parsing eller dataflow-analyse

Projektet demonstrerer således primært et kontrolleret workflow for et AI-agent-system fremfor perfekt sikkerhedsanalyse.

## 6. Evaluering

Systemet blev evalueret ved hjælp af faste test-repositories og prædefinerede testcases.

Evalueringen omfattede blandt andet:
- repositories med forventede vulnerabilities
- repositories uden fund
- falske positiver
- falske negativer
- deduplikering af fund
- fejlhåndtering
- ugyldigt JSON-output fra LLM’en

Projektet inkluderer blandt andet følgende typer testcases:
- repositories med hardkodede secrets
- repositories med SQL injection-møsntre
- sikre repositories uden fund
- repositories designet til at fremprovokere falske positiver
- repositories designet til at demonstrere falske negativer
- tomme repositories
- ugyldige repository paths

Evalueringen viste, at systemet generelt producerede verificerbare og konsistente resultater indenfor det afgrænsede scope.

Et vigtigt resultat var identificeringen af en falsk positiv i den første version af hardcoded secret-scanneren. Scanneren identificerede fejlagtigt en connection string hentet fra konfiguration som en hardcoded secret. Regex-reglen blev efterfølgende forbedret for at reducere denne type fejl.

Projektet demonstrerede også, at:
- LLM’en kunne returnere tomt JSON-output uden hallucinerede fund
- relaterede fund kunne kombineres
- ugyldigt JSON-output kunne opdages deterministisk
- logging af værktøjskald fungerede korrekt gennem hele workflowet

Den samlede evaluering understøtter, at systemet fungerer som et kontrolleret AI-agent-workflow med fokus på forklarlighed (explainability) og grounded reasoning.

---

## 7. Konklusion

Projektet demonstrerer, hvordan et moderne AI-agent-system kan kombinere deterministiske værktøjer med LLM-baseret ræsonnement og analyse til vurdering af problemer inden for sikker kodning.

Ved at adskille:
- scanning
- ræsonnement og analyse
- validering

opnår systemet et mere transparent og kontrolleret workflow end et rent LLM-baseret system.

Projektet viser samtidig både styrker og begrænsninger ved denne type AI-agentarkitektur. Deterministiske værktøjer forbedrer grounding og reducerer hallucinationsrisiko, men simple regex-baserede scannere giver stadig risiko for falske positiver og falske negativer.

Selvom systemet ikke er en produktionsklar sikkerhedsscanner, demonstrerer projektet centrale principper indenfor:
- AI agenter
- værktøjskald (tool-calling)
- grounded reasoning
- hallucinationsreduktion (hallucination mitigation)
- strukturerede output (structured outputs)
- deterministisk validering
- evaluering af agentadfærd

Projektet opfylder dermed formålet om at demonstrere et afgrænset, forklarligt og evaluerbart AI-agent-system.