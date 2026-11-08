# ledger_flex_re

Imaging of the main board of a Ledger Flex hardware wallet (PCB silkscreen
"LEDGER Rev. 5.2"), for hardware reverse-engineering and documentation.

## Origin

All images in this repository were taken by me, of a retail unit I purchased
from Ledger's official store on Amazon.

## Contents

| Path | Description |
|------|-------------|
| `xray/` | Raw X-ray images of the board (5 tiles, same magnification) |
| `xray_composite.png` | The X-ray tiles stitched into a single image |
| `pics/` | Raw optical microscope photos (RaySmart VMS700). The first two (`20261108_220839.JPG`, `20261108_220856.JPG`) are overviews of each side; the rest are close-ups |
| `board_sideA_stm32.jpg` | Stitched high-resolution view of side A (STM32WB35, ST25R3916), ~17310×11585 |
| `board_sideB_ledger.jpg` | Stitched high-resolution view of side B ("LEDGER" logo, debug pads), ~16740×11372 |
| `*_preview.jpg` | Downscaled (~2000 px wide) versions of the stitched views |
| `kicad/` | Work-in-progress KiCad reconstruction of the board (see below) |
| `docs/` | Renders and other documentation images |

## KiCad reconstruction (work in progress)

![3D render of the current KiCad board](docs/kicad_render_iso.png)

The board is being redrawn in KiCad 10 (`kicad/ledger_flex.kicad_pcb`). The
X-ray is the metric reference (29.09 px/mm, calibrated on the STM32's 0.5 mm
pin pitch). Both photo composites are warped onto it by matching vias and pads,
so all three views share one coordinate frame.

Current state:

- Board outline measured from the registered photos (47.0 × 31.3 mm), including
  the notches and recessed edge sections. The edge under the USB-C connector is
  approximate.
- Four plated mounting holes (3 × 3.0 mm, 1 × 1.5 mm).
- U1 STM32WB35CCU6A (QFN-48 7×7 mm), U2 secure element (WLCSP-24, 6×4 balls,
  0.4 mm pitch, 2.56 × 1.81 mm) and U3 ST25R3916 (WLCSP-36, 6×6 balls, 0.5 mm
  pitch). Placement checked against the X-ray. Ball A1 orientation of the two
  WLCSPs is not confirmed yet.
- The top photo, bottom photo (mirrored, as seen from the top) and X-ray are
  embedded as reference images on layers `User.1` to `User.3`. Higher
  resolution copies (100 px/mm, top-left corner at (100, 98) mm) are in
  `kicad/reference/`.
- The 4-layer stackup is a placeholder; the real layer count is not known yet.
- Remaining components, vias and traces are not drawn yet.

## Notes on the stitched images

- Composites were produced by feature matching and global alignment, with
  seam finding and multi-band blending.
- The close-ups do not cover the whole board. Areas without close-up coverage
  are filled from the upscaled overview photo and are noticeably softer.
- Background (mat) features do not line up between shots; only the board
  itself is aligned.

## License

Released under the MIT License, see [LICENSE](LICENSE).

"Ledger" and related names are trademarks of their respective owner. This
project is not affiliated with or endorsed by Ledger.
