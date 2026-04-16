# spec.md — <change-id>

## Title
<change title>

## Legacy context
This change touches the following legacy surfaces:
- <surface>
- <surface>

## Why now
<why this change matters now>

## In scope
- <item>
- <item>

## Out of scope
- full rewrite of <module>
- cleanup unrelated to affected paths

## Acceptance criteria
- [ ] [REQ-legacy-change-001] existing characterization tests still pass
- [ ] [REQ-legacy-change-002] no contract regressions on <boundary>
- [ ] [REQ-legacy-change-003] new behavior meets <criterion>
- [ ] [REQ-legacy-change-004] migration notes documented if applicable

## Traceability
- primary completion keys: requirement IDs above
- implementation evidence: <legacy files or new modules expected to cite relevant requirement IDs>
- verifier evidence: <characterization tests, regression tests, or manual records expected to cite relevant requirement IDs>
- generated reports: `generated/traceability/`

## Blast radius
- files/modules likely affected:
  - <path>
  - <path>

## Rollback trigger
Rollback if:
- <condition>
- <condition>
