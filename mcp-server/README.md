# 🤖 Intigriti MCP Server (Researcher API)

This subproject integrates a **Model Context Protocol (MCP)** server directly into the repository, allowing AI assistants (Claude Desktop, Antigravity, Cursor) to interface with the **Intigriti Researcher API v1.0**.

Collaborative architecture drawing from:
* [jdc94/mcp-intigriti-server](https://github.com/jdc94/mcp-intigriti-server)
* [alpernae/intigriti-mcp](https://github.com/alpernae/intigriti-mcp)

---

## ✨ Features

- **Scope Pre-Flight Checker (`validate_scope`)**: Prevents out-of-scope testing by validating targets against official asset rules before sending traffic.
- **Full OpenAPI Coverage**: Access programs, scopes, domains, and rules of engagement in real-time.
- **Activity Stream**: Monitor program announcements and scope updates.
- **Rate Limit & Error Resilient**: Built-in 429 backoff handling and structured error reporting.

---

## 🛠️ Prerequisites

- Python 3.10+
- Intigriti Researcher Account with API access enabled
- Personal Access Token from [app.intigriti.com](https://app.intigriti.com)

---

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and insert your personal token:
```bash
cp .env.example .env
```

---

## ⚙️ Connecting to AI Clients

### In Claude Desktop (`claude_desktop_config.json`)
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "intigriti": {
      "command": "python3",
      "args": ["/absolute/path/to/ethical-hacking-playbook/mcp-server/mcp_server.py"],
      "env": {
        "INTIGRITI_API_TOKEN": "YOUR_PERSONAL_ACCESS_TOKEN"
      }
    }
  }
}
```

### In Antigravity / Cursor
Register `mcp_server.py` as a local command-based MCP server in your workspace configuration with `INTIGRITI_API_TOKEN` populated.

---

## 🧰 Available Tools

| Tool | Description |
| :--- | :--- |
| `get_programs` | List accessible bug bounty programs with status and follow filters |
| `get_program_details` | Retrieve program metadata, reward tiers, and version IDs |
| `get_program_domains` | Fetch all in-scope and out-of-scope assets for a version |
| `get_program_rules_of_engagement` | Fetch testing rules, custom headers, and safe harbor constraints |
| `validate_scope` | **Pre-flight check**: Verify whether a hostname is authorized before testing |
| `get_program_activities` | Stream program announcements and scope revisions |
