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
  pitch). Placement checked against the X-ray. U1 pin 1 is at the package dot
  (bottom-left), U2 ball A1 at the dot printed on the board (top-left), and U3
  ball A1 at the dot on both the chip and the board (top-left).
- The top photo, bottom photo (mirrored, as seen from the top) and X-ray are
  embedded as reference images on layers `User.1` to `User.3`. Higher
  resolution copies (100 px/mm, top-left corner at (100, 98) mm) are in
  `kicad/reference/`.
- 159 through vias (0.2 mm drill, 0.4 mm pad). Each one was detected in the
  X-ray and confirmed by its hole showing in both photos.
- The five debug pads on the bottom side (TP1 to TP5). Names come from the
  nearest silkscreen label (RST, 3V0, IO, CLK); TP2 has no label.
- The five bottom-side connectors, with footprints measured from the photos:
  J1 board-to-board 2x12 at 0.35 mm pitch (Hirose BM28-style), J2 and J3
  board-to-board 2x3 at 0.4 mm pitch, J4 and J5 FPC connectors (6 and 4
  contacts, 0.5 mm pitch, flip lock). Exact part numbers are not identified,
  and connector pin numbers are arbitrary (row by row, left to right as seen
  from the top). The board-to-board receptacles (J1, J2, J3, J6) have 3D models
  built from the close-ups: housing with perimeter wall and central island,
  gold contacts in the groove, and the metal hold-down fittings. J2 and J3 are
  the same 2.55 × 3.95 mm part, rotated 90° from each other. Heights (0.6 to
  0.7 mm) are typical values, not measured.
- 226 passives and discretes (`tools/kicad/parts_passive.py`), read from
  gridded photo tiles of both sides (about ±0.1 mm). Two-terminal chips are
  prefixed `P` since R vs C is not known from photos; values are unknown. Body
  sizes were checked against the photos and the X-ray, where component bodies
  show clearly. Several resistors marked `000` and `01Z` are 0603 bodies on
  oversized 2.55 mm pad pairs, and are drawn that way. The diodes are a
  1.8 × 1.05 mm flat package with end terminals, not SOD-323F.
- The remaining ICs and parts, each with a footprint and 3D body at its
  measured size: U4 (marking 9420, 5×5 BGA at 0.4 mm pitch, balls located in
  the X-ray), U6 (ST, marking 022), U8 (marking VD1, 2×2 mm DFN-6 with exposed
  pad), U12 on the bottom (marking IDC 02), FL1 (8-terminal ceramic RF part
  next to the STM32), a 2.2 × 1.4 mm metal-lid part (U5), and several small
  leadless packages (Q1, Q2, U7, U9 to U11). Pin assignments of the unidentified
  parts are approximate.
- USB-C receptacle J7, mid-mount in a board cutout. Its 16-pin pad row and the
  four shell-leg slots are located in the X-ray.
- A sixth board-to-board connector J6 (2x3) on the bottom side, an unpopulated
  4-pad footprint, and the round gold test pads on both sides (TP6 to TP26).
- Hand-traced surface copper (`tools/kicad/tracks_manual.py`), each trace read
  from a high-zoom photo of its side and ending on a via or pad: the RST and
  3V0 debug pads, one STM32 pin, 8 traces from the J1 top row, short via stubs
  from the J1 bottom row, 3 from J4 and 2 from J2. Four traces from J1 end on
  passives that are not placed yet. Traces whose routing could not be read with
  confidence are left out.
- Four blind microvias (0.1 mm drill) where a surface trace ends on one.
- Most blind microvias (visible as dots in the photos) are not drawn yet.
- Board thickness is 0.8 mm. The 4-layer stackup is a placeholder; the real
  layer count is not known yet.
- Nets are not assigned and most traces are not drawn yet, so DRC reports
  clearance and dangling-via errors.

The board file is generated by `tools/kicad/build_board.py` (run with KiCad's
Python: `python3 tools/kicad/build_board.py kicad/ledger_flex.kicad_pcb
tools/kicad/refpng`). Outline, parts, vias and hand-traced tracks live in
`tools/kicad/outline_def.py`, `parts.py`, `vias_confirmed.json` and
`tracks_manual.py`.

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
