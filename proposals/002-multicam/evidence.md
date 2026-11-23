<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Multicam evidence and status

## Export survey

The source draft compares Avid Media Composer 2025.12.1, Premiere 27.1 beta and Resolve 21.1.1 exports of Trevor Aylward's edit. Only Avid AAF preserves both the shared definition and its selections. Flattened exports carry the chosen media but lose angle-switching intent. [Original Multicam draft](https://docs.google.com/document/d/1Gv2EX16aBOlTdI_3AbENFMdDbx65Fn95CE_neFbe4k4/edit), [fixture repository at cfda5d6](https://github.com/TrevorAyl/otio-multicam-tests/tree/cfda5d66b100c3bd1b4727887d64e96f6cc779d6)

| Export | Observed content | Reported size |
| --- | --- | ---: |
| Avid AAF | Per-cut Selectors with alternate slots and a shared backing composition | 2.1 MB |
| Avid OTIO | Ordinary clips for the active edit, with AAF metadata | 0.65 MB |
| Premiere OTIO | Each cut repeats all angle tracks. Active video angle is absent. | 54 MB |
| Premiere AAF | Flattened active media, with a graphics composition | 0.70 MB |
| Resolve OTIO | Repeated angle stacks with a shared Sequence ID and absent active selection | 25 MB |
| Resolve AAF | Flattened clips with source offsets that need relink verification | 0.71 MB |

Examples from the fixture include the first video and audio cuts lasting 38 and 37 frames respectively, angles assembled from several clips and gaps, and audio-only and video-only angles. Avid's mono groups select channel-by-channel, so higher channels can have fewer valid alternates. The graphics nest in Premiere and Resolve corresponds to separate fill and key angles in the Avid edit.

## Reference implementations

| Prototype | Reviewed head | Reported evidence |
| --- | --- | --- |
| [C++/Python #2](https://github.com/jhodges10/OpenTimelineIO/pull/2) | [59d0b93](https://github.com/jhodges10/OpenTimelineIO/commit/59d0b9319fe811dae110bbf6ad6bc7a69e63edd8) | Reads the Avid fixture using pyaaf2. Reports one definition, 13 angles and 62 cuts, with flatten matching Avid's export on all five tracks. Reports 13 new passing tests and a version-map test failure that also occurs on clean main in the same environment. |
| [Rust #139](https://github.com/alchemist-editor/otio-rust/pull/139) | [84bf169](https://github.com/alchemist-editor/otio-rust/commit/84bf16978848a02bbc0d7ffa533ed20c865a3a3f) | Reports cross-implementation serialization and flatten agreement on the synthetic and Avid fixtures. Opt-in AAF reads preserve the group and selections. Write/read tests preserve angles and cuts. Ordinary reads match the flattened path and invalid angle track selections are rejected. |

**Both PRs are prototypes for design feedback. Do not merge.**

The source document's Rust status predates the opt-in AAF reader and writer in #139. That PR also reports core, AAF and C ABI tests, with Go and TypeScript/wasm coverage. Its AAF round-trip evidence comes from adapter tests. Import of a generated AAF into Media Composer, Rust Python bindings, native Premiere and Resolve mapping, and FCPXML round trips remain open. [Rust ADR 0014](https://github.com/alchemist-editor/otio-rust/blob/84bf16978848a02bbc0d7ffa533ed20c865a3a3f/docs/adr/0014-multicam-prototype.md)

## Draft history

- **November 4, 2026** First draft based on upstream issue #427 and the Avid, Premiere and Resolve exports.
- **November 10, 2026** Separated design, adapter mapping and evidence and linked both prototypes.
