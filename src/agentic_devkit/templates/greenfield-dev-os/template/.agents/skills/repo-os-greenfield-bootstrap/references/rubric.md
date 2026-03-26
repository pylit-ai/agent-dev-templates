# Greenfield bootstrap rubric

Use this when filling placeholders so output stays consistent.

## NORTHSTAR.md
- Mission: one sentence, &lt;product&gt; for &lt;user&gt; so they can &lt;outcome&gt; with less &lt;pain&gt;.
- Non-goals: at least two; use "We are not building X" / "We will not optimize for Y in v1."

## PRD.md
- At least one primary and one secondary user.
- At least three in-scope items and two out-of-scope.
- User stories: "As a &lt;user&gt;, I want &lt;capability&gt;, so that &lt;benefit&gt;."

## specs/001-bootstrap
- In scope: concrete capabilities that match PRD.
- Acceptance criteria: objective pass/fail; each must be verifiable.
- Required verifiers: state unit/integration/manual per spec.

## AGENTS.md commands
- Must match actual repo: if there is a Makefile, use `make setup` etc.; if npm, use `npm run`; if uv, use `uv run`. Do not leave stub commands if the repo already has real ones.
