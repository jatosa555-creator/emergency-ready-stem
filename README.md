# Emergency-Ready STEM

**Emergency-Ready STEM Learning Design for Well-being and Resilience**

Thai-first teacher assistance for continuity planning, inclusive STEM lessons and return to learning. Four skills and one public read-only knowledge MCP. Publisher: **CHANON PHAJUNDA**.

## Source and service

- Canonical source: this repository; `plugin/` is the portable plugin source.
- `remote-mcp/`: bounded Netlify service; `knowledge/`: human-readable original guidance.
- MCP: https://emergency-ready-stem-knowledge.netlify.app/mcp · [health](https://emergency-ready-stem-knowledge.netlify.app/health). These are intended production URLs; verify current live evidence in release status.
- [Privacy](docs/privacy.md) · [Terms](docs/terms.md) · [Support](https://github.com/jatosa555-creator/emergency-ready-stem/issues).
- [Release status](docs/submission/RELEASE-STATUS.md) · [Workshop fallback](docs/WORKSHOP_TH.md).

The library contains original project guidance and labeled synthetic examples. It does not expose private Drive documents, third-party checklists, real student data or live emergency advisories. No accounts, write tools or tracking database. School authorities decide safety and reopening.

## Development

Node 22+: `cd remote-mcp`, `npm ci`, `npm test`, `npm run build`. Python 3.11+: install `requirements-dev.txt` for structural validators. The clean review ZIP is built by `python scripts/build_connected.py --demo-url ACTUAL_HTTPS_VIDEO_URL` after live verification. It includes only `plugin.json`, `mcp.json`, `assets/` and `skills/`. Never upload the historical developer handoff.

Git-linked Netlify builds use the root netlify.toml. `.netlify` is excluded from Git. No secrets are needed by the public knowledge service.
