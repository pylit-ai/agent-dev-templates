---
applyTo: "src/backend/**,src/api/**,tests/integration/**"
---

Follow `AGENTS.md` and `CONSTITUTION.md`.

Backend-specific rules:
- preserve backward compatibility unless the active spec explicitly approves a break
- boundary changes require integration tests
- add structured logs at external boundaries
- update contracts and migration notes when schemas or APIs change
