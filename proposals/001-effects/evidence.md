<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Effects evidence and status

## Survey

The source draft reports about 3,270 parameter instances across 302 catalogued effects in Premiere Pro 24.6, Resolve 19 and Media Composer 2025.12. It separately identifies 16 Hiero/Nuke Studio 15.1 soft effects pending cataloguing. The Avid extraction has 2,326 instances and contains unverified types, including likely toggles among nominal numbers. The cross-host linkage was preliminary. Only Gaussian Blur and Invert had two-host links in the database at the time of the draft. [Effects Schema draft](https://docs.google.com/document/d/1rI3j57z7eOfjFZSRJE4RTD2b-aSl55jnHxrYSkzhrGA/edit), [Vendor Effects database](https://airtable.com/appa6DhvJeNZSeDtj)

| Type | Premiere and Resolve census | Avid extraction |
| --- | ---: | ---: |
| Number | 394 | 1,452 (822 unverified) |
| Choice | 131 | 320 |
| Boolean | 122 | 186 |
| Percentage | 74 | 179 |
| 2D point | 60 | 27 |
| Angle | 54 | 4 |
| Nested group | 48 | 86 named categories |
| Color | 46 | 158 |
| Duration | 5 | 0 |
| Button or action | 5 | 0 |

The source observations motivate stable parameter keys, typed scalar and structured values, and portable spatial coordinates. The counts describe the survey, with limited evidence for any individual cross-host mapping.

## Reference implementations

| Prototype | Reviewed head | Scope |
| --- | --- | --- |
| [Rust #137](https://github.com/alchemist-editor/otio-rust/pull/137) | [ba87e3e](https://github.com/alchemist-editor/otio-rust/commit/ba87e3e615932d4cbd47c587e05be84d3190bb34) | Core schemas, downgrade, plugin and hook, reference registry, C ABI, SDKs and tests. |
| [C++/Python #1](https://github.com/jhodges10/OpenTimelineIO/pull/1) | [832ecb7](https://github.com/jhodges10/OpenTimelineIO/commit/832ecb706b7c9c061c81a429c82d1b25d7bd149a) | Upstream-style core and binding implementation, version maps, plugin behavior and test baselines. |

**Both PRs are prototypes for design feedback. Do not merge.**

The PRs implement the Effect.2 and Transition.2 version bumps described in the proposal. The implementation-status section of the original document describes an earlier subclass experiment. Use the PRs for the current prototype scope.

Rust #137 reports 979 Rust workspace tests passing, 519 upstream Python tests passing and 237 of 238 binding tests passing. The remaining binding failure concerns enum pickle bytes. Swift, Zig, C# and Objective-C SDKs were regenerated but were still awaiting local build verification in the PR report. The two experiments cover downgrade and upgrade, hook ordering, opt-in linking, data-driven mappings and round trips. Adapter interoperability and native rendering equivalence still need validation. [Rust test report](https://github.com/alchemist-editor/otio-rust/pull/137), [C++/Python test report](https://github.com/jhodges10/OpenTimelineIO/pull/1)

## Draft history

- **June 2026** Initial design discussion.
- **October 14, 2026** Revised to Effect.2 with one optional effect on Transition.2. Added spatial values, common color definitions and a value-space curve, and narrowed context and generator handling.
- **October 19, 2026** Added interoperable blur edge modes and separated registry and evidence.
- **October 23, 2026** Added read-time effects linkers and a reference linker.
- **November 10, 2026** Added links to both prototypes.
