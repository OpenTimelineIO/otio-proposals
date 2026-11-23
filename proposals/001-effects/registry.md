<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Common effect registry

The draft reserves `otio.fx.*` for registered operations. The definition document would record an ID, canonical context, display name, version, parameter types, units, defaults, advisory ranges and host mappings. The registry entry version goes in `effect_version`. Additive changes can extend a compatible entry. Removing or retyping a parameter requires a major version change. A reader that encounters an unsupported major version preserves the effect and its source data as transport-only.

## Proposed first roster

These are candidate entries. Vendor counterparts and their fidelity still need evidence, including for entries with worked definitions. [Source registry draft](https://docs.google.com/document/d/1rI3j57z7eOfjFZSRJE4RTD2b-aSl55jnHxrYSkzhrGA/edit)

| ID suffix under `otio.fx.` | Context | Core keys |
| --- | --- | --- |
| `transform_2d` | filter | position, anchor, scale_x, scale_y, rotation |
| `crop` | filter | left, right, top, bottom, softness |
| `flip` | filter | horizontal, vertical |
| `gaussian_blur` | filter | amount, horizontal, vertical, edge_mode |
| `color_cdl` | filter | slope, offset, power, saturation |
| `lut` | filter | lut_ref |
| `brightness_contrast` | filter | brightness, contrast, pivot |
| `levels` | filter | input_black, input_white, gamma, output_black, output_white |
| `rgb_curves` | filter | master, red, green, blue |
| `opacity` | filter | opacity, blend_mode |
| `timecode_burn_in` | filter | format, position, size, opacity |
| `dissolve` | transition | curve, reverse |
| `dip_to_color` | transition | color, reverse |
| `wipe` | transition | smpte_wipe_code, angle, softness, border_width, border_color, reverse |
| `push` | transition | direction, reverse |
| `audio_cross_fade` | transition | curve, level_offset_db |
| `audio_gain` | filter | gain_db |

The draft proposes a reverse control across transitions, while the worked audio cross-fade definition omits it. Resolve that difference before freezing the registry. Transition offsets provide alignment. The LUT entry covers file-based lookups. One-sided fades to or from color require a Gap in the current timeline model.

## Worked definitions

| Entry | Defaults and operation |
| --- | --- |
| `transform_2d` | Position and anchor default to center. Scale defaults to 100 percent on each axis. Rotation defaults to zero degrees, counterclockwise positive. Apply anchor, scale, rotation, then position. Convert native origins and axes on export. |
| `gaussian_blur` | Zero spatial-unit radius, both axes enabled. Default edge mode is `transparent`. Other values are `black`, `repeat`, `mirror` and `wrap`. Black samples outside as opaque black, while transparent samples zero alpha. Non-Gaussian kernels need an approximation flag or native transport. |
| `wipe` | `smpte_wipe_code` defaults to 0. A positive code takes precedence over angle, whose zero direction is left to right. Softness and border width default to zero in spatial units. Border color defaults to black and reverse to false. |
| `audio_cross_fade` | Default `constant_power` curve and zero dB midpoint offset. The other proposed curves are `linear` and `exponential`. |
| `brightness_contrast` | Defaults are zero brightness, contrast gain 1 and pivot 0.5. The signal formula is `(in - pivot) * contrast + pivot + brightness`. |
| `levels` | Input and output black/white default to 0/1 and gamma to 1. Use master values with optional channel overrides. |
| `rgb_curves` | Four normalized value-space curves default to identity. Apply master to all channels, then per-channel curves. |

Primary color parameters refer to the host working signal with black at 0 and white at 1. Conversions between different working spaces can be approximate. The [prototype registry JSON](https://github.com/alchemist-editor/otio-rust/blob/ba87e3e615932d4cbd47c587e05be84d3190bb34/crates/otio-adapter/data/otio_fx_registry.json) is review evidence. Its display-name matches are seeds for testing the linker.
