<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# OTIP-001 · Effects Schema

| Field | Value |
| --- | --- |
| OTIP | OTIP-001 |
| Status | Draft |
| Type | Standards Track |
| Author | Jeff Hodges |
| Created | 2026-10-14 |

## Summary

Extend `Effect` and `Transition` so editors and adapters can exchange a stable effect identity, provenance and typed static parameters. A small common registry gives widely used effects shared meanings. Optional read-time effects linkers translate host-native effects while preserving the native state needed for round trips.

[Original Effects Schema draft](https://docs.google.com/document/d/1rI3j57z7eOfjFZSRJE4RTD2b-aSl55jnHxrYSkzhrGA/edit) · [Registry](registry.md) · [Adapter mapping](adapter-mapping.md) · [Evidence and prototype status](evidence.md)

## Motivation and scope

Existing OTIO already carries effect placement and order, transition timing and enable state, retimes, and generator parameters. It generally leaves effect configuration in vendor metadata. Resolve, AAF and FCP 7 XML each preserve different native forms. Several adapters reduce wipes and other transitions to dissolves or carry the operation in metadata alone.

The draft identifies effects and parameter keys independently of localized UI names, records the source host and version, and specifies resolution-independent spatial values. Writers include defaults explicitly because host defaults can change. Track kind provides the media kind. Attachment and transition offsets already express routing, duration and alignment. [Effects discussion](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/discussions/921), [OpenFX contexts](https://openfx.readthedocs.io/en/latest/Reference/ofxImageEffectContexts.html)

Static transport and common mapping are in scope. Keyframes, graphs and multiple inputs, masks, effects with an independent timeline extent, metadata-driven expressions, shared effect instances and ACES/AMF colorspace operations are deferred. Static parameter values survive trims, moves and retimes unchanged. Transition progress continues to come from its offsets. [Temporal serialization discussion](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/331)

## Proposed interchange

### Effect.2

Keep the fields and behavior of Effect.1 and add the following fields. A blank `effect_id` represents a legacy effect. Use one effect type across old and new files. The draft author's earlier `ParameterizedEffect.1` approach was replaced in the draft. TimeEffect, LinearTimeWarp and FreezeFrame would remain at schema version 1, inherit the fields and leave them empty for retimes. Subclass versioning remains open for review.

| Field | Type and default | Meaning |
| --- | --- | --- |
| `effect_id` | string, empty | Stable operation ID. Use a reverse-DNS ID for a plugin, a registered `otio.fx.*` ID, or a vendor-specific ID. |
| `effect_version` | string, empty | Version of the operation or registry entry whose parameters were written. |
| `host` | string, empty | Host that produced the values. |
| `host_version` | string, empty | Version of that host. |
| `context` | string, empty | When set, `filter`, `transition` or `generator`, consistent with the attachment. |
| `parameters` | dictionary, empty | Values keyed by stable script name. Include values at their defaults. |

Register generator IDs through the existing `GeneratorReference.generator_kind` field and retain the existing generator parameters dictionary.

### Transition.2

Add one optional `effect` field containing an Effect, defaulting to null. An attached Effect.2 may set `context` to `transition` or leave it empty. Keep `transition_type` as the coarse fallback. Use `SMPTE_Dissolve` for dissolve-like transitions and `Custom_Transition` for other operations. With no effect attached, interpret `SMPTE_Dissolve` as the default `otio.fx.dissolve` on video or default `otio.fx.audio_cross_fade` on audio. Existing transition placement, offsets and enable state keep their meanings.

### Parameter values

- Store numbers, booleans and strings directly. Encode a choice by its stable option string.
- Use type-tagged dictionaries for a spatial `2D XY` point, a non-spatial `2D` pair, `color`, or a `curve`. Nested parameter groups are untagged dictionaries.
- Spatial coordinates are unitless, center-origin and positive up, mapped through `available_image_bounds`. A `2D XY px` value carries `x`, `y` and authoring `resolution` as an approximate fallback. Spatial scalars use the same OTIO units. [OTIO spatial coordinates](https://opentimelineio.readthedocs.io/en/stable/tutorials/spatial-coordinates.html)
- Color values carry `red`, `green`, `blue`, optional `alpha` and optional `colorspace` with sRGB as the default. A value-space curve carries sorted, normalized input/output point pairs and `linear` or monotone-cubic `spline` interpolation.
- Skip buttons and actions. Ranges and UI precision belong in definitions or the application. The draft uses RationalTime for durations expressed in seconds, pending the temporal design.

## Compatibility and interoperability

Upgrade ordinary Effect.1 and Transition.1 with empty fields. A downgrade moves Effect.2 additions to `metadata["otio.fx"]` and the Transition.2 effect to `metadata["otio.fx"]["effect"]`. An upgrader restores these values from the downgrade envelope and retains unrelated metadata. Lossless restoration assumes the interchange path preserves that metadata. Older readers can retain unknown schema data where supported. For readers that require known schema versions, serialize the downgrade explicitly.

A host's same-format writer should prefer its preserved native state. Other readers use the standard parameters where they can. See the [adapter mapping and fidelity rules](adapter-mapping.md).

### Effects linkers

Add an `effects_linkers` manifest list of `EffectsLinker.1` plugins. A plugin's `link_effect(in_effect, parent, effects_linker_argument_map)` receives the effect plus the containing Item or Transition, and returns a replacement or `None` to retain it. The walk covers Item effects and attached transition effects.

After adapter read and `post_adapter_read`, run media linking and `post_media_linker`, then effects linking and `post_effects_linker`. Pass the effects linker arguments to the hook as well. `read_from_file` and `read_from_string` accept `effects_linker_name` and `effects_linker_argument_map`. Name lookup and `EffectsLinkingPolicy` follow media linkers, including `DoNotLinkEffects`, `ForceDefaultLinker` and `OTIO_DEFAULT_EFFECTS_LINKER`. With no explicit selection or default, behavior is unchanged. The built-in `otio_fx_registry` reference linker is opt-in.

A mapping replaces the ID, version and parameters with canonical values. It preserves source host fields and stores original ID, version, parameters and linker name in `metadata["otio.fx"]["linked_from"]`. Mark inexact mappings as `approximate` under `metadata["otio.fx"]["fidelity"]`. Generators continue to use media linkers. On write, the adapter maps canonical operations into its format. Sites can use existing `pre_adapter_write` hooks.

## Examples

- [Effect.2 picture-in-picture](examples/effect-v2.otio) uses canonical transform parameters and marks the illustrative native metadata.
- [Transition.2 wipe](examples/transition-v2.otio) attaches an Effect.2 with SMPTE wipe code 1 and keeps the transition offsets.

The examples are serialized schema objects for review with a reader that implements this draft.

## Implementation and evidence

Both implementations are **experimental draft prototypes for feedback. Do not merge.** [Rust, C ABI and SDKs](https://github.com/alchemist-editor/otio-rust/pull/137), [C++ and Python](https://github.com/jhodges10/OpenTimelineIO/pull/1)

See [evidence and status](evidence.md) for prototype revisions, test reports and the adapter survey. There is no technical dependency on OTIP-002.

## Open questions for the TSC

- Should retime subclasses bump versions? Should the single attached effect eventually replace `transition_type`?
- Should explicit context remain, and do generators need separate identity or provenance fields?
- Where should the registry live, who approves entries, and how many independently documented mappings should an entry need?
- Should registry definitions use plain JSON or schema-defined objects? Should fidelity become a schema field?
- Should percent and degrees stay registry-defined units? Should approximate pixel points be accepted?
- Should there be a dedicated write-side linker?
