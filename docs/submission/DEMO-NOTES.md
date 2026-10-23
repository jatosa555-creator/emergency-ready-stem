# Walkthrough provenance

The video is a timed sequence of unaltered screenshots captured through the browser UI from the live production `/demo.html` on 2026-10-23. Each step actually called the public MCP; the timestamps and HTTP responses are visible. It is a protocol/service walkthrough, not a fabricated ChatGPT conversation or evidence of teacher/classroom success.

Sequence: source scope → offline-topic search → exact original item ER-02 and citation → synthetic example ER-04 → missing ER-99 → nonexistent write tool rejected. The demo page can repeat these calls for reviewers without credentials. Host model behavior and free-account access must be tested separately against the supplied eight review prompts.

Rebuild: capture six actual states as `remote-mcp/artifacts/demo/step-1.png` through `step-6.png` with CUA, then run `python scripts/build_demo_video.py` with FFmpeg installed. Never replace the frames with imagined model responses. The final public video is part of the Netlify static service deployment.
