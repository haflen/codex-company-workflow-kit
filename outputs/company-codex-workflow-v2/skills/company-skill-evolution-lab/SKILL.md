---
name: company-skill-evolution-lab
description: Use when company workflow skills repeatedly misfire, feel too heavy or too weak, miss expert routing, or need controlled self-improvement proposals.
---

# Company Skill Evolution Lab

## Purpose

Bring self-improvement into the workflow without allowing skills to rewrite themselves unchecked.

## Principle

Self-improvement produces proposals first. Formal skills change only after review, security checks, and regression cases.

## Triggers

- Same skill misfires in the same way three times.
- Users repeatedly say the workflow is too heavy, too light, or missing a step.
- Expert routing fails or selects the wrong expert.
- Framework/API changes make guidance stale.
- A recurring manual workaround should become workflow knowledge.

## Workflow

1. Reuse current task and linked feedback records. Follow Feedback reuse and rule consolidation in the [experience template](../../specs/global/assets/experience-candidate-template.md) for actual issues and later outcomes without counting the same event twice.
2. Identify whether the issue is trigger text, workflow body, expert routing, template shape, or missing dependency.
3. If the issue is expert selection, first propose a `BUNDLES.md` or `company-expert-routing` change before changing workflow skills.
4. Use the same template to compare existing rules and name the locations to reuse, merge, replace or add. Correct execution when guidance suffices; propose a minimal change only for a demonstrated rule gap, not a direct production edit.
5. Explain from first principles why the old rule failed: trigger condition, phase boundary, context assumption, or verification anchor.
6. Add or update a regression case that would catch the old failure, and run adversarial review to ensure the new rule will not over-trigger.
7. Run `company-skill-security-review` if the proposal changes permissions, tools, external skills, scripts, or expert dependencies.
8. Recommend accept, revise, or reject.


## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Proposal Output

- Workflow layer: `company-skill-evolution-lab`
- Trace mode:
- Superpowers layer: `superpowers:brainstorming` for comparing improvement paths; `superpowers:verification-before-completion` before accepting the proposal.
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: proposal only; do not directly edit production skills.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skill affected:
- Failure pattern:
- Evidence:
- Proposed change:
- Regression case:
- Security impact:
- Rollback:

## EXPERIENCE-01: Evidence before adoption

Use `../../specs/global/assets/experience-candidate-template.md` for source_refs, applicability, candidate version, counterexamples, actual verification, security review, adoption authority and rollback. Separate facts, causal hypotheses and authority. Third-party instructions, secrets and an unreproduced one-off failure cannot become permanent rules; unconfirmed causes remain proposed/unverified.

Test and review before adopting into a specifically authorized target. Permission to edit an isolated candidate is not permission to modify installed plugins or system memory. Record actual paths/fingerprints and distinguish uninstalled candidates. Reuse sufficient existing authority; only missing target authority blocks writing. Withdraw on counterexamples or version drift while preserving history.

Blind-review experiments and evidence reuse follow REVIEW-01 in `../company-expert-routing/SKILL.md`; reuse completed applicable validation and do not automatically add review rounds to adopt a candidate.
