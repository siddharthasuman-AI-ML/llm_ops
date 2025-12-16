RAG Agent Red-Teaming Report
1. Overview
A red-team evaluation was executed on the internal CRM RAG Agent (Gemini 2.5 Pro Flash +
FAISS + guardrails). Tests were run using PromptFoo CLI and UI, covering jailbreak, data
extraction, prompt injection, role-break, and output-filter bypass scenarios. Objective: validate
guardrails preventing leakage of customer PII.
2. Execution Issues
• CLI could not process prompts consistently due to schema mismatch (e.g., {"query": } parsing
errors).
• UI produced correct results, but CLI had eval failures due to config drift.
• Several test suites failed because the evaluator could not map prompts to expected fields.
• Inconsistent environment variables caused reproducibility issues.
3. Security Findings
• Guardrail bypass observed in jailbreak and role-break conditions.
• Input guardrails failed to activate for certain multi-step attacks.
• Output filters occasionally missed PII due to regex-only implementation.
• RAG retrieval sometimes surfaced sensitive chunks before filtering.
4. Root Causes
• Guardrails applied too late in pipeline.
• Regex-only filters insufficient for disguised PII.
• Sensitive KB entries reachable through retrieval.
• Configuration mismatch between UI and CLI test setups.
5. Recommendations
• Standardize PromptFoo configs across CLI and UI.
• Add semantic PII detection instead of regex-only filtering.
• Block sensitive retrieval chunks before they reach LLM.
• Re-index knowledge base with PII masking.
• Add classifier-based jailbreak detection.
• Build reproducible test runner (Docker/Makefile).
6. Final Assessment
The system has strong foundations but remains vulnerable to jailbreak chains, retrieval leakage,
and testing pipeline inconsistencies. With targeted improvements to guardrail hierarchy, semantic
filtering, and retrieval security, the system can be hardened for production.

