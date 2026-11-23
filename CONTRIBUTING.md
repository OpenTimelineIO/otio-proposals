<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Contributing

Use this repository for significant schema, interoperability or process changes. Use the [OpenTimelineIO issue tracker](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues) for bugs and isolated changes to the core library. Schema proposals should follow the existing [schema development guidance](https://opentimelineio.readthedocs.io/en/stable/tutorials/developing-a-new-schema.html) alongside the draft process in [OTIP-000](proposals/000-process/README.md).

## Submit a proposal

1. Fork this repository and copy the [template](templates/proposal.md) to `proposals/draft-<slug>/README.md`. Use `Unassigned` for the OTIP and `To do` for the initial status.
2. Open a draft pull request. Link the rendered Markdown, related discussions and supporting evidence. Keep each PR focused on one proposal. Document dependencies explicitly when proposals are related.
3. Discuss the design in the PR. A proposal editor or TSC-designated maintainer assigns a number after triage. Rename the directory to `proposals/NNN-<slug>/`, set the OTIP field to `OTIP-NNN` and add its index row with the proposal.
4. Include serialized examples for schema changes. Describe upgrade, downgrade, legacy reader behavior and adapter fidelity. Link prototype PRs as evidence and label their merge intent. Keep implementation code in the implementation repositories.

Run `python3 tools/check_proposals.py` from the repository root. It checks proposal IDs, metadata, index coverage, relative link targets and JSON example syntax.

## Project policies

Follow the [OpenTimelineIO code of conduct](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/CODE_OF_CONDUCT.md) and the [TSC charter](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/tsc/OpenTimelineIO_TSC_Charter.md#7-intellectual-property-policy). Submit material you have the right to contribute. See the [license terms](LICENSE.md) for documentation, examples and tooling.

The charter requires a contributor license agreement (CLA) and Developer Certificate of Origin (DCO) sign-off for code contributions. Follow [OpenTimelineIO's CLA instructions](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/CONTRIBUTING.md#contributor-license-agreement). Use `git commit -s` when you can make the [DCO certification](https://developercertificate.org/) for your contribution.
