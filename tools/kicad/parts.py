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
 # further ICs and parts, sized from the photos and the X-ray (pin 1 / ball A1 top-left where marked)
 ('ledger_flex', 'BGA-25_2.15x2.1mm_Layout5x5_P0.4mm', 'U4', 'marking 9420 2710', 107.67, 122.25, 0, 'F'),
 ('ledger_flex', '2T_2.2x1.4mm_MetalLid', 'U5', '2-terminal, grey metal lid', 110.06, 121.44, 0, 'F'),
 ('ledger_flex', 'DFN-6_2.1x1.45mm_P0.4mm', 'U6', 'ST, marking 022', 108.15, 126.33, 0, 'F'),
 ('ledger_flex', 'DFN-3_0.7x0.7mm', 'Q1', '3-pad, dark body', 117.09, 114.43, 0, 'F'),
 ('ledger_flex', 'WLCSP-4_1.2x1.15mm', 'U7', '4-pad die', 120.05, 124.50, 0, 'F'),
 ('ledger_flex', 'RF_Ceramic_2.05x1.25mm_8T', 'FL1', 'RF ceramic (filter/balun)', 132.40, 112.35, 0, 'F'),
 ('ledger_flex', 'DFN-6-1EP_1.85x1.95mm_P0.5mm', 'U8', 'marking VD1 0AP', 146.88, 123.56, 0, 'F'),
 ('ledger_flex', 'DFN-4_0.65x0.67mm', 'U9', 'small 4-pad', 145.00, 123.12, 0, 'F'),
 ('ledger_flex', 'DFN-6_0.65x0.8mm', 'U10', 'small 6-pad', 145.05, 128.98, 0, 'F'),
 ('ledger_flex', 'LGA-4_0.48x0.65mm_PadsOutside', 'U11', 'small 4-pad, grey', 114.33, 112.13, 0, 'F'),
 ('ledger_flex', 'USB_C_Receptacle_MidMount_16P_measured', 'J7', 'USB-C receptacle (mid-mount)', 108.85, 112.83, 0, 'F'),
 ('ledger_flex', 'TestPad_D1.1mm', 'TP6', '', 114.80, 123.62, 0, 'F', True),
 ('ledger_flex', 'SON-6-2T_2.05x1.95mm_P0.5mm', 'U12', 'marking IDC 02 S0', 141.95, 118.88, 0, 'B'),
 ('ledger_flex', 'DFN-3_0.83x1.17mm', 'Q2', '3-pad', 125.11, 123.64, 0, 'B'),
 ('ledger_flex', 'BtB_2x3_P0.35mm_C_measured', 'J6', 'BtB 2x3 ~0.36mm', 140.64, 108.38, 0, 'B'),
 ('ledger_flex', 'Pads_2x2_0.65x0.45mm_Unpopulated', 'U13', 'unpopulated 4-pad footprint', 135.42, 112.35, 0, 'B'),
 ('ledger_flex', 'TestPad_Square0.6mm', 'TP7', '', 139.50, 113.17, 0, 'B', True),
 ('ledger_flex', 'TestPad_D1.5mm', 'TP8', '', 114.88, 123.65, 0, 'B', True),
]
# round gold test pads on the bottom side (about 1.1 mm)
TP_B = [(116.77, 109.13), (116.88, 111.81), (141.67, 114.19), (114.33, 120.45), (110.70, 121.42), (116.70, 121.70),
        (121.72, 120.15), (136.96, 121.40), (146.69, 121.75), (147.21, 119.43), (145.52, 123.77), (137.41, 124.15),
        (140.28, 125.00), (138.29, 126.77), (144.26, 128.92), (108.92, 129.20), (105.85, 123.57), (107.88, 124.50)]
PARTS += [('ledger_flex', 'TestPad_D1.1mm', f'TP{9 + i}', '', x, y, 0, 'B', True) for i, (x, y) in enumerate(TP_B)]
