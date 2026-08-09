# Security

## Threat model (summary)

Blender MCP connects an AI client to Blender over a local TCP bridge and may call third-party 3D APIs with **user-supplied** keys.

| Asset | Risk if leaked | Mitigation |
|-------|----------------|------------|
| Sketchfab / Hyper3D / Hunyuan keys | Billable API abuse | OS-backed vault (`secret_store`), PASSWORD prefs, avoid scene/`.blend` storage |
| LLM API keys (Claude, etc.) | Account takeover | **Not read by this package** — stay in the MCP client |
| Prompts / executed Python | IP + accidental secrets in text | Telemetry opt-in; **redact** secret-shaped strings before upload |
| Local TCP `:9876` | Local code exec in Blender | Default bind localhost; treat `execute_blender_code` as powerful |

## Telemetry

- Endpoint is configured via `config.py` / env (`BLENDER_MCP_SUPABASE_URL`, publishable key only).
- **Never** ship `sb_secret` or database passwords in the client.
- Without consent: tool name, success, duration, platform, version only.
- With consent: prompts/code/metadata after **redaction** (`secret_redact.py`); flags `secret_like` + `secret_kinds` for research metrics — not raw keys.
- Opt out: `BLENDER_MCP_DISABLE_TELEMETRY=1` or uncheck addon consent.

## Reporting

Report vulnerabilities privately to the maintainers. Do not open public issues with live secrets.
