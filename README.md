# 🛡️ Ethical Hacking & Bug Bounty Playbook

A comprehensive, developer-first ethical hacking and vulnerability research repository based on **Intigriti's Researcher Terms & Conditions**, **Community Code of Conduct**, and international Safe Harbor standards.

Includes a built-in **Model Context Protocol (MCP) Server** for live Intigriti Researcher API integration (inspired by and collaborating with community projects [jdc94/mcp-intigriti-server](https://github.com/jdc94/mcp-intigriti-server) and [alpernae/intigriti-mcp](https://github.com/alpernae/intigriti-mcp)).

---

## 📌 Core Objectives

This repository serves as a permanent reference and operational toolkit for developers conducting vulnerability research, bug bounty hunting, and coordinated vulnerability disclosure (CVD). It defines the legal, ethical, and technical boundaries required to ensure testing remains **authorized, constructive, and legally protected**.

---

## ⚡ The 5 Golden Rules of Ethical Research

1. **Strict Scope Discipline**: Never send a packet to an asset that is not explicitly marked as **In-Scope** in the active program brief. If an asset is ambiguous, assume it is out of scope.
2. **Minimal Intrusion ("Stop When Proven")**: Exploit only to the bare minimum required to prove the vulnerability exists. As soon as impact is established, stop immediately.
3. **Absolute Data Protection (GDPR & PII)**: Never download, dump, copy, or browse personal or customer data. If PII is exposed, document the finding minimally, redact sensitive values, and report immediately.
4. **No Pivoting / Lateral Movement**: Once an authentication bypass, internal network access, admin panel, or remote shell is achieved, cease testing. Never pivot across internal infrastructure.
5. **Strict Confidentiality**: All program details, discovered bugs, client data, and triage discussions are confidential. Never disclose findings publicly without mutual written agreement via Intigriti.

---

## 🤖 Built-in Intigriti MCP Server

The repository includes a dedicated **Model Context Protocol (MCP)** server under [`mcp-server/`](mcp-server/) that connects AI coding assistants directly to Intigriti's Researcher API:

* **Live Program Queries**: Search programs, inspect reward tiers, and retrieve rules of engagement.
* **Scope Verification Tool (`validate_scope`)**: Programmatically verifies whether a domain or URL is authorized before sending traffic.
* **Activity & Triage Tracking**: Track live updates and announcements on followed programs.

See [mcp-server/README.md](mcp-server/README.md) for quick setup in Claude Desktop, Antigravity, or Cursor.

---

## 📚 Handbook Directory

| Document | Description |
| :--- | :--- |
| [🤖 MCP Server Guide](mcp-server/README.md) | Full setup and tool documentation for the Intigriti Researcher API MCP Server. |
| [📜 Rules of Engagement](docs/RULES_OF_ENGAGEMENT.md) | Breakdown of Intigriti's Researcher Terms & Conditions, legal protections, criminal law context, liabilities, and tax obligations. |
| [🤝 Community Code of Conduct](docs/CODE_OF_CONDUCT.md) | Behavioral standards, GDPR compliance, PII handling, PoC hosting rules, and sanctions. |
| [🛠️ Testing Methodology](docs/TESTING_METHODOLOGY.md) | Technical setup (Burp Suite proxy headers, test accounts), safe PoC benchmarks (SQLi, XSS, RCE, SSRF, IDOR), and non-destructive testing guidelines. |
| [📝 Vulnerability Submission Template](templates/SUBMISSION_TEMPLATE.md) | Production-ready report template designed for quick triage validation and clear remediation guidance. |

---

## 🚀 Pre-Flight Checklist (Run Before Every Session)

- [ ] **Program Status**: Is the program currently active on Intigriti?
- [ ] **Asset Validation**: Is the target domain/IP explicitly listed under *In-Scope* (use MCP `validate_scope`)?
- [ ] **Identification Header**: Is your proxy configured to inject the required header (e.g., `X-Intigriti-Username: <handle>`)?
- [ ] **Account Setup**: Are you using your `@intigriti.me` email and your own test accounts?
- [ ] **Out-of-Scope Checks**: Are you avoiding all program-excluded categories (e.g., DoS, social engineering, missing SPF/DKIM, generic rate limits)?
- [ ] **PoC Safety**: Are all payloads read-only and non-destructive?

---

## 🙏 Credits & Collaboration

The MCP server in this repository builds upon and credits community work:
* [jdc94/mcp-intigriti-server](https://github.com/jdc94/mcp-intigriti-server) by @jdc94
* [alpernae/intigriti-mcp](https://github.com/alpernae/intigriti-mcp) by @alpernae

---

## ⚖️ Legal Disclaimer

The methodologies, tools, and guidelines in this repository are intended strictly for educational purposes and authorized security research conducted within programs that provide explicit authorization (Safe Harbor). Unauthorized testing against computer systems without prior consent violates computer crime laws worldwide (including Belgian Criminal Code Article 550bis, the US Computer Fraud and Abuse Act 18 U.S.C. § 1030, and equivalent national statutes).
