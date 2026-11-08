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
