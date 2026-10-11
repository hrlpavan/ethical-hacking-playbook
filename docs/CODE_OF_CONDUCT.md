# 🤝 Community Code of Conduct & Operational Ethics

Based on **Intigriti's Community Code of Conduct** and industry best practices.

---

## 1. Data Exposure & PII Handling (GDPR Regulation EU 2016/679)

Assets in scope may contain Personally Identifiable Information (PII) or confidential client data. Stumbling across PII is a critical indicator of a vulnerability, not an invitation to collect data.

### Mandatory Rules for Encountering PII:
- **Zero Harvesting**: Never download, export, scrape, or retain customer records or database dumps.
- **Bare Minimum Exposure**: If an authorization flaw displays a user list, do not paginate through additional records.
- **No Local Storage**: Never save extracted PII to your local disk or cloud drives. If temporary artifacts are captured during HTTP proxy logging, delete them immediately after submitting the report.
- **Redaction Requirement**: When submitting screenshots or HTTP logs, redact or blur all PII (names, emails, phone numbers, addresses, authentication tokens).
- **Target Own Test Accounts Only**: Always simulate cross-user attacks between test accounts you control (e.g., User A accessing User B's resources).

---

## 2. Non-Intrusive Testing & Safe Commands

Always prioritize the stability, integrity, and availability of production environments:

* **Safe Database Inquiries**:
  * ✅ Use harmless read queries: `SELECT VERSION()`, `SELECT CURRENT_USER()`, or `SELECT DATABASE()`.
  * ❌ Prohibited: `DROP`, `DELETE`, `UPDATE`, `INSERT`, or full-table `UNION SELECT` dumps.
* **Safe Command Injection / RCE**:
  * ✅ Use benign identification commands: `whoami`, `id`, `hostname`.
  * ⚠️ Discouraged: `phpinfo()` (may leak sensitive API keys or environment secrets unless strictly necessary).
  * ❌ Prohibited: Launching reverse shells, reading sensitive credential files (`/etc/shadow`, AWS metadata endpoints), or writing persistent web shells.
* **Safe XSS Verification**:
  * ✅ Use non-destructive popups or logs: `console.log(document.domain)` or `alert(document.domain)`.
  * ❌ Prohibited: Harvesting `document.cookie` or redirection to credential-phishing pages.

---

## 3. Strict Pivoting Prohibition

When testing reveals an entry point into an authenticated backend, internal network, or server filesystem:

1. **Cease Testing Immediately**: Do not explore internal subnets, scan intranet IPs, or escalate privileges within the host OS.
2. **Submit Entry Point**: Report the initial compromise vector through Intigriti.
3. **Triage Assessment**: Intigriti and the vendor assess maximum impact based on the demonstrated entry point without requiring researchers to risk internal disruption.

---

## 4. Third-Party Hosting & Tool Restrictions

* **No Public Hosting of PoCs**: Never upload reproduction videos or PoC exploits to public platforms (e.g., unlisted YouTube videos, public GitHub gists, public Google Drive links).
* **Platform Attachments First**: Attach files directly inside the Intigriti report submission form.
* **Encrypted Archives**: If technical size limits require external transfer, host within a **password-protected ZIP archive** and include the decryption password inside the secret report.
* **Unapproved Third-Party Scanners**: Tools that store reproduction data or PII on unverified external servers (e.g., public XSS Hunter instances) are prohibited. Pingback services (like Burp Collaborator) are acceptable unless explicitly banned by program rules.

---

## 5. Professionalism & Anti-Fraud Standards

Intigriti enforces a zero-tolerance policy against toxic or deceptive practices:

* **No "Placeholder" Reports**: Submitting blank or incomplete reports to "reserve" a duplicate priority before another researcher submits is strictly prohibited.
* **No "Beg Bounties"**: Never demand compensation for unsolicited, low-value reports (such as missing security headers or public DNS records).
* **Respectful Communication**: Maintain professional dialogue with triagers and customer security teams. Never flood tickets or harass analysts.
* **No Scanner Spam**: Do not submit automated scanner dumps without manual verification and clear impact demonstration.

---

## 6. Sanction Framework

Violations of the Code of Conduct are reviewed by a community board of experts and penalized according to **Intent**, **Impact**, and **Recidivism**:

1. **Warning**: Formal notification with probation.
2. **Invitation Restriction**: Revocation of private program access and suspension from new invitations.
3. **Payment Restriction**: Forfeiture of monetary bounties for the duration of the sanction.
4. **Platform Ban**: Temporary or permanent termination of the researcher's Intigriti account.
