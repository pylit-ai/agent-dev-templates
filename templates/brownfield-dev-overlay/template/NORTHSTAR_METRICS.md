# NORTHSTAR_METRICS

<!--
  Verifier-aware metric system for AI coding-agent work in this repo.
  Draft or refine using the northstar-metric skill (metactl: `~/.metactl/skills/northstar-metric/SKILL.md`)
  or the `/northstar-metric` command. Do not treat raw benchmark scores as the objective.
-->

## A. Purpose and scope

**Purpose:** Define how we measure success for autonomous coding-agent tasks without collapsing multi-dimensional quality into a single hackable score.

**In scope:** <tasks / workflows agents run, e.g. specs, bugs, migrations>.

**Out of scope:** <what this document does not govern, e.g. human hiring metrics>.

**Relationship to other docs:** Product intent lives in `NORTHSTAR.md`. This file owns **gates vs optimized metrics vs diagnostics** for agent/eval loops. If product vision and metrics conflict, `NORTHSTAR.md` wins.

## B. True objective and non-goals

**True objective (plain language):** <what “winning” means for users or operators>.

**What we can verify vs estimate:** <binary checks, rubrics, subjective judgment>.

**Non-goals for this metric system:**

- We will not optimize: <e.g. raw leaderboard score without gates>.
- We will not fold into one scalar: <hard safety / integrity gates>.

## C. Task taxonomy and horizon buckets

| Bucket   | Definition                         | Examples                          |
| -------- | ---------------------------------- | --------------------------------- |
| Short    | <e.g. one session / under N turns> | <bugfix, tiny PR>                 |
| Medium   | <definition>                       | <feature slice>                   |
| Long     | <definition>                       | <multi-spec migration>            |

**Classes (if useful):** Requirement-completion (new capability) vs regression-preservation (safety of existing behavior) — <how you split>.

## D. Hard gates / invariants

These **MUST** pass before any headline or composite score is reported as success. They are **not** weighted into the northstar.

| Gate ID | Invariant              | Verifier / signal        | Failure = block |
| ------- | ---------------------- | ------------------------ | --------------- |
| G-001   | <e.g. CI green>        | <CI / tests>             | yes             |
| G-002   | <e.g. security policy> | <scanner / review>       | yes             |
| G-003   | <e.g. no secret leak>  | <gitleaks / policy>      | yes             |

Add rows until gates match `CONSTITUTION.md` and real repo risk.

## E. Headline northstar metric

**Definition (gate-qualified):** Rate of **fresh tasks** that achieve **trusted resolution** within **budget** after **all hard gates (§D) pass**.

| Field        | Specification                                                                        |
| ------------ | ------------------------------------------------------------------------------------ |
| Numerator    | Count of tasks with trusted resolution (define “trusted” below)                    |
| Denominator  | Count of fresh tasks attempted in scope (define “fresh”)                           |
| Unit         | <e.g. proportion per week, or count/month>                                           |
| Budget       | <wall time, $, token budget, max iterations>                                         |
| Trusted resolution | <e.g. merge + CI + reviewer rubric threshold; not self-reported alone>       |
| Reporting    | **By horizon bucket (§C)** and overall                                               |

**Explicit formula (replace with numbers when known):**

\[
\text{NS} = \frac{\text{\# tasks passing §D with trusted resolution within budget}}{\text{\# fresh tasks in scope}}
\]

**Why not a raw KPI:** <one sentence — optimization pressure must not erode gates or holdouts>.

## F. Supporting metrics

Each row: optimized **or** monitored — never mix gates in here.

| Name | Intent | Formula | Unit | Data source | Grader | Trust | Role (opt / monitor) | Gaming risk | Cadence | Owner role |
| ---- | ------ | ------- | ---- | ----------- | ------ | ----- | -------------------- | ----------- | ------- | ---------- |
| <M1> | <…>    | <…>     | <…>  | <…>         | <…>    | <…>   | <…>                  | <…>         | <…>     | <…>        |

**Categories to fill as needed:**

- Quality (human or rubric)
- Reliability (flake rate, repro)
- Efficiency (latency, tokens, cost per task)
- Process (e.g. spec closure rate)

## G. Diagnostics and anti-hacking metrics

Independent signals not directly maximized; detect **false progress** and **evaluator gaming**.

| Diagnostic | What it catches | Data source | Alert threshold |
| ---------- | --------------- | ----------- | --------------- |
| <D1>       | <e.g. train/holdout gap> | <…> | <…> |
| <D2>       | <e.g. judge vs test disagreement> | <…> | <…> |

**Evaluator integrity:** <frozen eval sets, rotation, cross-check models, human audit sample>.

## H. Progressive curriculum / maturity ladder

| Stage | Scope unlocked | Metric bar to advance |
| ----- | -------------- | --------------------- |
| 0     | <sandbox / stubs> | <…>                   |
| 1     | <single package>   | <…>                   |
| 2     | <production path>  | <…>                   |

## I. Loop-closure process

- **Failure → artifact:** Flakes, bugs, and disagreements become <new tests, rubric items, red-team tasks, ticket templates>.
- **Regression:** When <supporting metric or holdout> drops, <who investigates, SLA>.
- **Score drops:** <trigger for halt / spec for harness change>.

## J. Stopping criteria and “no longer making progress”

Stop or reset the optimization loop when:

- <Plateau: holdout flat for N cycles while cost rises>.
- <Reliability: flake or revert rate exceeds threshold>.
- <Integrity: rising mismatch between gates and manual audit>.
- <Meltdown: repeated loops without new real resolution>.

## K. Anti-Goodhart / anti-paperclip analysis

| Likely hack                | Mitigation in this system                          | Residual risk                          |
| -------------------------- | -------------------------------------------------- | -------------------------------------- |
| <e.g. narrow test fitting> | <holdouts, independence, gates>                    | <what remains>                         |
| <e.g. judge pleasing>      | <cross-verifiers, audits>                          | <…>                                    |

**Uncovered dimensions:** <honest list>.

## L. Review cadence and change control

- **Review:** <e.g. quarterly> with `NORTHSTAR.md` and `PRD.md` when scope shifts.
- **Change control:** Updates to headline definition or gates require <e.g. RFC + owner sign-off>.
- **Version:** Bump a short changelog at bottom when definitions change.

---

## Assumptions and evidence (fill on first real pass)

| Assumption | Confidence | Evidence needed |
| ---------- | ---------- | --------------- |
| <…>       | low/med/high | <…>             |

---

## Changelog

| Date | Change |
| ---- | ------ |
| <initial> | Template seeded from repo OS; replace placeholders. |
