<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# OTIP-002 · Multicam Schema

| Field | Value |
| --- | --- |
| OTIP | OTIP-002 |
| Status | Draft |
| Type | Standards Track |
| Author | Jeff Hodges |
| Created | 2026-11-04 |

## Summary

Store each synchronized multicam once in `Timeline.multicams` and put a `MulticamClip.1` in a regular track for each cut. Every cut names the selected angle and, where needed, selects one of that angle's audio tracks. Picture and each sound track can switch at independent frames.

[Original Multicam draft](https://docs.google.com/document/d/1Gv2EX16aBOlTdI_3AbENFMdDbx65Fn95CE_neFbe4k4/edit) · [Adapter mapping](adapter-mapping.md) · [Evidence and prototype status](evidence.md)

## Motivation and scope

Today's OTIO exports either flatten multicam to ordinary clips or duplicate all angles at each cut. The latter can keep angle material while omitting the live selection. Avid AAF and FCPXML each provide precedent for a shared definition and per-cut selection. In one source edit, Premiere OTIO is 54 MB and Resolve OTIO is 25 MB, with all angles repeated at each cut. The Avid AAF is 2.1 MB and stores selections and shared definitions. [Upstream Multicam discussion](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/427), [export evidence](evidence.md)

The design must preserve one definition, the selected angle and per-kind track at each cut, independent audio and video timing, and angles containing multiple clips, gaps or nested compositions. It must provide a standard flattening path. Angle identity is independent of display order and native IDs. The definition can carry sync-start timecode. Cycles and unresolved selections are invalid.

Defer sync method, audio-follows-video editing policy, rendering of fill/key effects, channel layouts inside a multichannel clip and cross-file definitions. Independent multicam interchange and flattening have no dependency on OTIP-001. Recreating a native matte key in an edit may also need an effects interchange design.

## Proposed interchange

### Timeline.multicams

Add an optional dictionary from string key to `Multicam.1`. Writers choose stable keys within the timeline, for example an AAF MobID, a Resolve sequence ID or a disambiguated name. A missing dictionary means empty. Omit it when empty so serialization for files without multicam can remain unchanged. The proposal retains `Timeline.1`.

The dictionary holds definitions outside the track tree. References are explicit keys and work independently of OTIO's optional object-instancing support.

### Multicam.1

Use a Stack-derived Composition held in the timeline dictionary. Its children are angle Stacks in display order. The inherited `name` is a display label, and `metadata` can carry native identifiers or sync details. An optional `global_start_time` is the source timecode at multicam time zero.

Each angle's Stack name must be unique within its definition and serves as the reference target. Each angle holds at most one Video track and any number of Audio tracks. Tracks share a multicam time coordinate and may hold media, gaps, nests or cuts to another multicam. An angle can supply picture only, sound only or both.

### MulticamClip.1

A cut is an Item in an ordinary track. It inherits the Item fields, including `source_range`, `enabled`, `effects`, `markers` and `metadata`.

| Field | Type | Meaning |
| --- | --- | --- |
| `multicam` | string | Required key into the containing timeline's definitions. |
| `angle` | string | Required name of the selected angle Stack. |
| `angle_track` | nonnegative integer, default 0 | Zero-based index among the selected angle's tracks of the enclosing track's kind. On an audio track, 3 selects the fourth audio track. |
| `source_range` | TimeRange | Slice in multicam coordinates, inherited from Item. Its start and duration stay fixed when switching angles. |

Selection is fixed over one Item. Cut again to switch, and resolve the enclosing track's kind before interpreting `angle_track`. Validate that the target definition, angle and track exist, angle names are unique, and definition references are acyclic, including nested cuts. The original proposal describes the available range as the multicam duration. The C++ prototype needs a timeline to resolve that range and raises on direct `available_range()` calls. The resolution API and validation timing remain for review. [C++ prototype](https://github.com/jhodges10/OpenTimelineIO/pull/2)

## Compatibility and flattening

Use the timeline and selected angle track to resolve each cut. Flattening replaces it with ordinary items for the slice it plays, including gaps and multiple clips where needed. Resolve nested multicams, pad uncovered spans with gaps, remove the multicam definitions after replacement and return a loss report for discarded editability or unsupported data. The prototypes differ on whether flatten returns a copy or operates in place. The flattened interchange result and loss reporting are the common design requirement.

The root stays a Timeline, which keeps ordinary timelines on the existing schema. A legacy reader can still reject the unknown MulticamClip in a track. Write a flattened timeline for older OTIO versions and delivery formats that lack native multicam. Flattening preserves the active edit and discards the ability to switch to alternate angles. [Format behavior and limitations](adapter-mapping.md)

## Example

[Two-angle Timeline.1 with independent picture and audio cuts](examples/multicam-v1.otio) is a complete synthetic JSON example at 24 fps. Video switches from A to B at frame 24. Audio switches at frame 20 from A's second audio track to B's first. Angle B's video starts with an eight-frame gap. The video switch lands 16 frames into B's media-segment range, while the audio resolves independently. One shared definition serves all four cuts.

## Implementation and evidence

Both implementations are **experimental draft prototypes for feedback. Do not merge.** [Rust, C ABI and SDKs](https://github.com/alchemist-editor/otio-rust/pull/139), [C++ and Python](https://github.com/jhodges10/OpenTimelineIO/pull/2)

The prototypes demonstrate Avid AAF import and flattening of a 13-angle, 62-cut edit. Rust also reports AAF write/read tests. A generated AAF still needs to be imported into Media Composer. [Evidence and revisions](evidence.md)

## Open questions for the TSC

- Should Stack name remain the stable angle key, or should an explicit ID allow renames without rewriting cuts?
- Should the first version support bin or cross-file definitions, or remain timeline-local? Is an embedded flattened fallback worth duplication and drift?
- Where should readers validate, and how should a caller obtain the context-dependent available range?
- Should audio-follows-video remain an editorial workflow setting?
- Does the proposed stacked-cut interpretation of Avid fill/key edits match editorial intent? Do Resolve AAF multicam-relative offsets relink to the correct frames?
