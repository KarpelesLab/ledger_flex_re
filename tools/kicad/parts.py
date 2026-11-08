# (lib, footprint, ref, value, x, y, rotation_deg, side)
PARTS = [
 ('Package_DFN_QFN', 'QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm', 'U1', 'STM32WB35CCU6A', 122.30, 112.63, 90, 'F'),
 ('ledger_flex', 'WLCSP-24_2.56x1.81mm_Layout6x4_P0.4mm', 'U2', 'SE (ST33, marking KC7A6)', 134.72, 118.73, 0, 'F'),
 ('ledger_flex', 'WLCSP-36_3.2x3.2mm_Layout6x6_P0.5mm', 'U3', 'ST25R3916', 141.55, 118.62, 0, 'F'),
 # debug pads on the bottom side; names from the nearest silkscreen label (TP2 has no label)
 ('ledger_flex', 'TestPad_D1.0mm', 'TP1', 'RST', 117.08, 105.29, 0, 'B'),
 ('ledger_flex', 'TestPad_D1.0mm', 'TP2', 'unlabeled', 119.05, 105.29, 0, 'B'),
 ('ledger_flex', 'TestPad_D1.0mm', 'TP3', '3V0', 121.01, 105.29, 0, 'B'),
 ('ledger_flex', 'TestPad_D1.0mm', 'TP4', 'IO', 118.08, 106.97, 0, 'B'),
 ('ledger_flex', 'TestPad_D1.0mm', 'TP5', 'CLK', 120.04, 106.97, 0, 'B'),
]
