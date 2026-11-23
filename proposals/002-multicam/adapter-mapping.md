<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Multicam adapter mapping

Native multicam interchange requires a shared definition, per-cut sources and enough timing data to identify the selected angle and track. When only the active edit can be represented, flatten and surface the loss report.

| Format | Read | Write and limits |
| --- | --- | --- |
| Avid AAF | Map a group/backing composition to a shared Multicam. Group its slots into angles, using slot names or the underlying master clip. A cut's Selector supplies the selected angle, per-kind track and multicam-relative source range. Rust exposes this behind an opt-in read setting. | Write a backing composition, group composition and one Selector per cut. Alternate tracks represent other available angles at the same position. Regular readers take the selected branch. Rust reports write/read tests. Import into Media Composer remains unverified. |
| FCPXML | Map `media/multicam` and `mc-angle` to the definition and angles. Map `tcStart` to `global_start_time` and `mc-source` selections to per-track cuts. | Pair video and audio selections into a single `mc-clip` when their ranges align. Use separate `mc-clip` selections where needed. Proposed mapping needs fixtures and round-trip testing. |
| FCP 7 XML | Assess `multiclip` with active video and audio angles against real exports. | Write native multiclip only after validation. Otherwise flatten. |
| Resolve OTIO | The surveyed `Sequence Type` and `Sequence ID` metadata identify related copied Stacks. The files omit the chosen angle, so deduplication alone cannot recover the edit. | Write the new schema when the destination supports it. Otherwise flatten. Validate Resolve AAF source offsets against relinked media before using them to recover selection. |
| Premiere OTIO | The surveyed nested stacks omit multicam identity and live angle. Audio channel metadata alone cannot reconstruct cuts. | Flatten for current export paths. Pairing OTIO structure with flattened AAF selection is an investigation. |
| EDL, ALE and older OTIO | Existing ordinary clip behavior. | Flatten before writing and keep the loss report. |

Adobe and Blackmagic can improve interchange by exporting per-cut live angle and channel, ideally with a stable reference to one shared definition. Tests should include independent picture and audio switches, missing channels, angle gaps, nested content and native round trips. [Source mapping](https://docs.google.com/document/d/1Gv2EX16aBOlTdI_3AbENFMdDbx65Fn95CE_neFbe4k4/edit), [Rust AAF design and limits](https://github.com/alchemist-editor/otio-rust/blob/84bf16978848a02bbc0d7ffa533ed20c865a3a3f/docs/adr/0014-multicam-prototype.md)
