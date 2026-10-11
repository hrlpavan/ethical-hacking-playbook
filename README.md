# 🛡️ Ethical Hacking & Bug Bounty Playbook

A comprehensive, developer-first ethical hacking and vulnerability research guide based on **Intigriti's Researcher Terms & Conditions**, **Community Code of Conduct**, and international Safe Harbor standards.

---

## 📌 Core Objectives

This repository serves as a permanent reference for developers conducting vulnerability research, bug bounty hunting, and coordinated vulnerability disclosure (CVD). It defines the legal, ethical, and technical boundaries required to ensure testing remains **authorized, constructive, and legally protected**.

---

## ⚡ The 5 Golden Rules of Ethical Research

1. **Strict Scope Discipline**: Never send a packet to an asset that is not explicitly marked as **In-Scope** in the active program brief. If an asset is ambiguous, assume it is out of scope.
2. **Minimal Intrusion ("Stop When Proven")**: Exploit only to the bare minimum required to prove the vulnerability exists. As soon as impact is established, stop immediately.
3. **Absolute Data Protection (GDPR & PII)**: Never download, dump, copy, or browse personal or customer data. If PII is exposed, document the finding minimally, redact sensitive values, and report immediately.
4. **No Pivoting / Lateral Movement**: Once an authentication bypass, internal network access, admin panel, or remote shell is achieved, cease testing. Never pivot across internal infrastructure.
5. **Strict Confidentiality**: All program details, discovered bugs, client data, and triage discussions are confidential. Never disclose findings publicly without mutual written agreement via Intigriti.

---

## 📚 Handbook Directory

| Document | Description |
| :--- | :--- |
| [📜 Rules of Engagement](docs/RULES_OF_ENGAGEMENT.md) | Full breakdown of Intigriti's Researcher Terms & Conditions, legal protections, criminal law context, liabilities, and tax obligations. |
| [🤝 Community Code of Conduct](docs/CODE_OF_CONDUCT.md) | Behavioral standards, GDPR compliance, PII handling, PoC hosting rules, and sanctions. |
| [🛠️ Testing Methodology](docs/TESTING_METHODOLOGY.md) | Technical setup (Burp Suite proxy headers, test accounts), safe PoC benchmarks (SQLi, XSS, RCE, SSRF, IDOR), and non-destructive testing guidelines. |
| [📝 Vulnerability Submission Template](templates/SUBMISSION_TEMPLATE.md) | Production-ready report template designed for quick triage validation and clear remediation guidance. |

---

## 🚀 Pre-Flight Checklist (Run Before Every Session)

- [ ] **Program Status**: Is the program currently active on Intigriti?
- [ ] **Asset Validation**: Is the target domain/IP explicitly listed under *In-Scope*?
- [ ] **Identification Header**: Is your proxy configured to inject the required header (e.g., `X-Intigriti-Username: <handle>`)?
- [ ] **Account Setup**: Are you using your `@intigriti.me` email and your own test accounts?
- [ ] **Out-of-Scope Checks**: Are you avoiding all program-excluded categories (e.g., DoS, social engineering, missing SPF/DKIM, generic rate limits)?
- [ ] **PoC Safety**: Are all payloads read-only and non-destructive?

---

## ⚖️ Legal Disclaimer

The methodologies and guidelines in this repository are intended strictly for educational purposes and authorized security research conducted within programs that provide explicit authorization (Safe Harbor). Unauthorized testing against computer systems without prior consent violates computer crime laws worldwide (including Belgian Criminal Code Article 550bis, the US Computer Fraud and Abuse Act 18 U.S.C. § 1030, and equivalent national statutes).
