# Document Ownership and Record Size

Business ownership determines location; behavior change and risk determine record size. A release batch does not redefine ownership. Apply this policy with document-standard.md; it adds no skill or approval stage.

## Before Writing: Scope to the Current Work

1. Read the INDEX ownership map, current task, and directly related module/version entry, not the entire repository.
2. Reuse the existing work-item-id and authoritative record first. Establish owner-path (owning directory), record-path (this record), and release-target (delivery batch, possibly undecided). Put these in existing internal task/execution-record metadata, not a separate checklist file; before writing, retain them in working context.
3. If the project uses version/milestone directories, inherit the feature owner. Small size, a new branch, or a later date does not justify a new root specs/features/ directory. Preserve an explicitly adopted feature layout; do not force versions on it. For a new project with no convention, confirm the layout once.
4. Shared authentication, build, and governance work use the existing shared owner. If no owner exists or candidates conflict, ask only about ownership rather than guessing the latest version. Do not create a permanent document package until resolved; read-only analysis may continue.
5. Later phases inherit the decision; revisit only when scope or ownership evidence changes. This check grants no authority to implement, relocate files, commit, or release.

## Choose Record Size Automatically

| Situation | Record |
| --- | --- |
| Omission or implementation defect in an unaccepted task | Update that task and its verification record; no separate bugfix package |
| Low-risk repair of an existing feature, with no changed business promise | Add a stable-ID entry to its existing fix log; if absent, create one compact fix record |
| Few changed lines but permissions, money/formulas, migration, cross-system or other high risk | Keep the owner; add necessary focused design, rollback, and verification evidence; never lower verification because of line count |
| New capability or changed approved business rules | Route through requirements/design change, update affected authority, and confirm before implementation |
| Repair shared by multiple versions | One authoritative record, linked from affected versions and release lists; no duplicate bodies |

An internal compact record contains work-item-id, owner-path, record-path, release-target, problem/expected behavior, scope, verification evidence/unverified items, current status, and next step. Reuse existing metadata instead of duplicating it. Do not require a requirements/design/tasks trio. Formal requirements, designs, and formal fix records still follow their diagram requirements in document-standard.md; lightweight does not waive diagrams or real API acceptance.

Record classification: an entry in an existing task/fix log checks traceability, diagram consistency, verification, and drift within the touched scope, not a full historical-log rewrite. A new standalone formal fix report includes a decision summary and a Mermaid problem-to-cause-to-fix-to-verification diagram. Update affected original requirements/design diagrams; a compact entry cannot replace them. Do not redraw unaffected diagrams.

Human documents retain only task identifiers, scope, results, and evidence needed by readers, without copying internal ownership inventories. Apply human-output-standard.md.

## Closeout and History

- Separate implementation, verification, commit, merge, and deployment states. Update only evidence-backed changes; a commit is not proof of deployment.
- Do not silently rewrite accepted/released baselines. Link the baseline from the fix record and explain the change; explicitly record the comparison baseline when correcting the current authoritative specification.
- Preserve dated historical conclusions. Update README/task entries that represent current status and link fresh evidence; do not leave an obsolete "not committed" claim as current fact.
- Update INDEX, project overview, and version README only when navigation, scope, phase, or release state changes. Follow public-document branch policy: business branches use a public-doc patch, not a direct promotion of local progress to mainline status.
- Health checks report misplaced records, duplicated authority, broken links, and stale current status only. Before migration, list old-to-new paths and affected references; move only with user authorization. Do not renumber, delete history, or overwrite business content automatically.
- Passing asset-path checks does not prove document ownership. This is a semantic workflow check, not a claim that existing scripts automatically validate business ownership.

## Acceptance Scenarios

| Scenario | Required outcome |
| --- | --- |
| OWN-01 Small legend repair in an existing version | Keep original module; compact record; no new root features directory |
| OWN-02 Omission in an unaccepted task | Update original task; no parallel requirements package |
| OWN-03 Two-line money formula repair | Same owner; high-risk verification retained |
| OWN-04 Shared login repair across versions | One shared authority; references instead of copies |
| OWN-05 Old feature shipped in a later release | owner-path does not follow release-target; release list links the repair |
| OWN-06 Unknown owner or mixed historical layouts | Preserve state and clarify ownership; no automatic migration or repository-wide rewrite |
