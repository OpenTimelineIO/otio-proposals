<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# OTIP-000 · Proposal process and governance

| Field | Value |
| --- | --- |
| OTIP | OTIP-000 |
| Status | Draft |
| Type | Process |
| Author | Jeff Hodges |
| Created | 2026-11-23 |

## Summary

Use an OpenUSD-style public review process for significant OpenTimelineIO design and process changes. Each proposal gets a permanent identifier and one directory. The proposal PR records review and publication. Separate implementation PRs record delivery.

## Existing decisions and project policy

- The November 19, 2026 TSC notes record the name `otio-proposals` under the schema proposal repository agenda item. [November 19 TSC notes](https://docs.google.com/document/d/1L4Y_qfVc1lEyHNdpHA-Lrnzb2DEhO77OQq3rxVli4a4/edit)
- The OpenTimelineIO charter establishes TSC oversight and the project's decision-making rules. Existing upstream schema-development guidance continues to apply. [TSC charter](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/tsc/OpenTimelineIO_TSC_Charter.md), [schema development workflow](https://opentimelineio.readthedocs.io/en/stable/tutorials/developing-a-new-schema.html)
- The repository bootstrap uses the requested three-digit identifier convention and reserves OTIP-000 for this process, OTIP-001 for Effects Schema and OTIP-002 for Multicam Schema. Those assignments acknowledge the subjects of the drafts.

## Recommended process

The following workflow is proposed for TSC adoption. The [OpenUSD proposal process](https://github.com/PixarAnimationStudios/OpenUSD-proposals/blob/main/README.md) is the precedent for proposal directories, review in PRs and separate publication and implementation milestones.

### Scope and roles

Use an OTIP for changes to serialized schemas, interchange contracts, broad API behavior or project processes. The author owns the draft and addresses review. Community reviewers contribute use cases, implementer feedback and interoperability evidence. A proposal editor designated by the TSC would triage scope, assign IDs, keep the index current and help the author obtain review. The TSC would make the publication decision under its charter. A committer would record the decision and merge the proposal PR after approval.

### IDs and files

Open a draft PR from the [template](../../templates/proposal.md) in `proposals/draft-<slug>/`. After triage, an editor would assign the next unused three-digit number and update the directory name to `proposals/NNN-<slug>/`. Use `OTIP-NNN` in formal references. Keep the assigned number and path stable after triage, even if the title changes or the proposal is closed or superseded. Never recycle a number. For a closed, unpublished draft, preserve its ID and PR link in the index or an index follow-up.

Include a `README.md` in every proposal directory. Keep reviewable supporting material with the proposal. Large changes may use an umbrella proposal and independently reviewable proposals with explicit dependencies. Use the [index](../README.md) for durable discovery.

### Review and publication

| Status | Meaning |
| --- | --- |
| To do | Draft PR opened for triage. The problem and scope can still change. |
| Draft | Initial design is available for public review. The author tracks and addresses feedback in the PR. |
| Hold | The PR stays open with a written blocker and restart condition. Resume at Draft when the blocker is resolved. |
| Finalizing | The author has addressed substantive feedback and summarized the remaining trade-offs and review outcome. |
| Published | The TSC has approved the design and a committer has merged the proposal with a link to that decision. |
| Implemented | A follow-up records the release that ships the design, along with implementation links and any limits. |
| Closed | The PR records that the proposal was withdrawn or declined, with the rationale where available. |
| Superseded | A follow-up to a published proposal links the approved successor. |

GitHub draft and ready-for-review states control notifications. The OTIP's status in the document records where the design is in this lifecycle. Discuss decisions on the proposal PR and link related upstream discussions, TSC minutes or mailing-list records. During finalization the author should show concrete examples, compatibility, the effect on adapters and the evidence for trade-offs. Recommend public notice before finalization closes and a decision recorded in the PR under the charter's consensus or voting process. This draft delegates the exact review window and editor appointment to the TSC.

### Versions and implementation

An OTIP ID stays stable across editorial revisions, which Git records. Serialized types keep their independent schema versions, such as `Effect.2`. An implementation may have its own version or release tag. Record all three where applicable. A substantive revision after publication should get a new review. Use a new OTIP with a supersession link when a change revises the accepted interchange contract.

Keep code reviews and releases in the appropriate implementation repositories. Prototypes can demonstrate feasibility during review. Label experimental PRs with their merge intent and record the tested revision, evidence and gaps. Move to Implemented only once the tracked release is available.

## Open questions for the TSC

- Who should serve as proposal editor and who can assign numbers when the editor is unavailable?
- Should finalization have a minimum public review period?
- What interoperability evidence should be required for a schema proposal to publish?

OTIP-000 itself is subject to TSC review under the existing charter.
