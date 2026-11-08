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
 # connectors on the bottom side (positions = centre of the contact pattern)
 ('ledger_flex', 'BtB_2x12_P0.35mm_measured', 'J1', 'BtB 2x12 0.35mm (Hirose BM28-style)', 134.06, 126.47, 0, 'B'),
 ('ledger_flex', 'BtB_2x3_P0.4mm_A_measured', 'J2', 'BtB 2x3 0.4mm', 106.85, 127.19, 0, 'B'),
 ('ledger_flex', 'BtB_2x3_P0.4mm_B_measured', 'J3', 'BtB 2x3 0.4mm', 146.45, 127.67, 0, 'B'),
 ('ledger_flex', 'FPC_1x06_P0.5mm_measured', 'J4', 'FPC 6-pin 0.5mm', 119.025, 123.55, 0, 'B'),
 ('ledger_flex', 'FPC_1x04_P0.5mm_measured', 'J5', 'FPC 4-pin 0.5mm', 141.40, 126.55, 0, 'B'),
]
