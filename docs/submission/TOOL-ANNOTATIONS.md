# Tool annotations and reviewer access

All three tools have the same truthful annotations:

- `readOnlyHint=true`: searches and reads a fixed public JSON snapshot. No data mutations.
- `destructiveHint=false`: no write, deletion, school system access or actions on behalf of a user.
- `idempotentHint=true`: the same arguments against the same deployed snapshot return the same content.
- `openWorldHint=false`: no runtime external fetch, private Drive, arbitrary URL, file path or user resource access. Citation URLs are returned as text; the tool does not fetch them.

No authentication or test account is required. The service is deliberately public within the owner's authorized original guidance scope. This is not a private document service. Unknown item IDs return `found=false`; malformed IDs and extraneous arguments are rejected by strict schemas. All tool requests have a 16 KiB cap and topic searches a 160-character cap. Netlify's IP/domain rate limit is declared at the `/mcp` function (120 requests / 60 seconds), not an in-memory imitation. Infrastructure limits may also apply.

Safe review sequence: `list_collections {}` → `search_references {"query":"ออฟไลน์","limit":3}` → `get_reference {"id":"ER-02"}`. Check `ER-04` for a labeled synthetic dataset. Check `ER-99` for a real missing-item response. No tool should be called with personal data.

The eight review prompts describe intended model behavior. Backend tests do not establish that the model follows each prompt; record actual host results separately. No commerce is supported.
