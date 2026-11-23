<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Effects adapter mapping

A recognizing writer should emit the registry ID, entry version and every canonical parameter in registry units. Preserve the source application's full state under its usual metadata namespace, including native identity and keyframes where the adapter already carries them. A same-host writer prefers its native block where it can restore the operation. For a cross-host mapping, use the shared parameters and record approximate fidelity for incomplete or inexact conversion. Keep unrecognized effects as transport-only.

| Format or host | Existing behavior reported in the source draft | Proposed mapping and limits |
| --- | --- | --- |
| Avid AAF | OperationGroup metadata preserves native state. The surveyed adapter reduces transitions to a dissolve on read. | Preserve OperationGroup metadata. Normalize known DVE position, scale and rotation with axis conversion, and map wipe families by code or angle when verified. Report approximate Avid blur edge handling until its behavior is confirmed. |
| FCP 7 XML | Native effect subtrees can carry details, while the surveyed adapter reduces transitions to a dissolve. | Translate supported wipe codes to and from `smpte_wipe_code` and retain the native subtree. |
| CMX 3600 EDL | The surveyed adapter preserves the wipe code in `cmx_3600` metadata. | Map a supported W code to the registered wipe and keep the original metadata. The code can round-trip when the target supports it. |
| Resolve OTIO | `Resolve_OTIO` carries parameter, variant and keyframe data. | Use known OpenFX identity or verified registry mappings. Preserve native values. Convert documented border modes to canonical blur modes and flag cross-kernel or working-space approximations. |
| Premiere Pro | Native Motion coordinates use a top-left origin with positive down. | Convert to OTIO spatial coordinates. Map Gaussian Blur's Repeat Edge Pixels switch to `repeat` or `transparent` and verify the parameter conversion. |
| Hiero / Nuke Studio | Transform and color soft effects cover some of the roster. Nuke blur can sample beyond the bounding box. | Convert verified Transform and Grade values, distinguish replicated edges from BlackOutside behavior, and retain unsupported soft-effect constructs in native metadata. |

Registry transforms and blur handling are specified in [worked definitions](registry.md). Prefer stable native IDs over display names when a host provides them. Mapping tables need a review of native parameter keys, host versions, units and fixture fidelity. The reference linker's initial seeds exercise dispatch and skip logic.

Sources include the [Effects Schema draft](https://docs.google.com/document/d/1rI3j57z7eOfjFZSRJE4RTD2b-aSl55jnHxrYSkzhrGA/edit), [AMWA AAF Effects Protocol](https://www.amwa.tv/_files/ugd/f66d69_898ba231b4224b0280bb7ce9ce607a89.pdf), [Foundry Transform discussion](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/discussions/1794), and [Nuke bounding box documentation](https://learn.foundry.com/NUKE/content/comp_environment/reformatting_elements/adjusting_bbox.html).
