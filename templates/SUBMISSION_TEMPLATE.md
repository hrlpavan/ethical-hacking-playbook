# 📝 Intigriti Vulnerability Submission Template

Use this template to prepare comprehensive, triager-friendly vulnerability reports.

---

```markdown
# [Vulnerability Type] in [Component / Endpoint]

## 1. Summary
A brief 2–3 sentence overview explaining the vulnerability, the vulnerable component, and the real-world security impact.

* **Target Asset**: [e.g., *.adobe.com / specific domain]
* **Vulnerability Class**: [e.g., CWE-639: Broken Object Level Authorization (IDOR)]
* **Severity Estimate**: [Low / Medium / High / Critical]
* **CVSS v3.1 Vector**: [e.g., CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N]

---

## 2. In-Scope Validation
- [x] Verified that the target asset is explicitly listed as in-scope on the program detail page.
- [x] Confirmed that testing adhered to the Rules of Engagement and Safe Harbor guidelines.
- [x] Testing traffic included the required identification header: `X-Intigriti-Username: <username>`

---

## 3. Test Environment & Accounts Used
* **Attacker Account**: `user_a@intigriti.me` (ID: `1001`)
* **Victim / Secondary Account**: `user_b@intigriti.me` (ID: `2002`)
* **Client / Browser Version**: [e.g., Firefox 128 / Burp Suite]

---

## 4. Step-by-Step Reproduction Instructions

1. Log in to the application using the **Victim Account** (`user_b@intigriti.me`).
2. Navigate to `https://target.com/settings/projects` and create a private project named `Confidential Project`.
3. Note the generated project ID: `2002`.
4. Log out and log in using the **Attacker Account** (`user_a@intigriti.me`).
5. Send the following HTTP request modifying the `projectId` parameter to `2002`:

```http
POST /api/v1/projects/delete HTTP/1.1
Host: target.com
Authorization: Bearer <User_A_Token>
Content-Type: application/json
X-Intigriti-Username: <your-username>

{
  "projectId": "2002"
}
```

6. Observe that the server responds with `200 OK` and the victim's project `2002` is deleted.

---

## 5. Proof of Concept (PoC)

### Request:
```http
[Insert sanitized, reproducible HTTP request]
```

### Response:
```http
[Insert sanitized HTTP response with PII redacted]
```

*(Attach non-sensitive screenshots or an encrypted PoC archive if applicable).*

---

## 6. Security Impact
Explain what an attacker can achieve in a realistic scenario:
- **Confidentiality**: [Can an unauthorized user access private data?]
- **Integrity**: [Can an attacker modify or delete other users' records?]
- **Availability**: [Is service stability affected?]

---

## 7. Recommended Remediation
Provide code-level suggestions for the development team:
- Enforce server-side authorization checks verifying that the authenticated session (`req.user.id`) owns the requested resource before performing read/write operations.
- Example fix:
```python
# Verify ownership
project = get_project_by_id(project_id)
if project.owner_id != current_user.id:
    raise PermissionDenied("You do not have access to this resource.")
```
```
