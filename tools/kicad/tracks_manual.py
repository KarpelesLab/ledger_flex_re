# Hand-traced surface copper. Each entry was read from the high-zoom photo of its side
# (raised trace visible through the solder mask) and its endpoints match a via or pad.
# Endpoints marked "passive" end on a passive component pad that is not placed yet.
# (layer, width_mm, [(x, y), ...], note)
TRACKS = [
 # debug pads
 ('B.Cu', 0.10, [(117.08, 105.29), (117.835, 105.30), (119.056, 106.521)], 'TP1 (RST) -> through via'),
 ('B.Cu', 0.15, [(121.01, 105.29), (121.012, 106.21)], 'TP3 (3V0) -> through via'),
 ('F.Cu', 0.10, [(122.432, 106.534), (122.98, 107.08), (122.98, 108.75), (123.05, 108.95)], 'through via -> U1.29'),
 # J1 top row (bottom side)
 ('B.Cu', 0.10, [(132.13, 125.52), (132.15, 124.00), (131.91, 123.66), (131.91, 123.42)], 'J1.1 -> passive'),
 ('B.Cu', 0.10, [(132.48, 125.52), (132.48, 124.00), (132.42, 123.80), (132.42, 123.42)], 'J1.2 -> passive'),
 ('B.Cu', 0.10, [(132.83, 125.52), (132.83, 124.00), (132.90, 123.80), (132.90, 123.42)], 'J1.3 -> passive'),
 ('B.Cu', 0.10, [(133.18, 125.52), (133.18, 123.90), (133.42, 123.60), (133.42, 123.42)], 'J1.4 -> passive'),
 ('B.Cu', 0.10, [(133.533, 125.52), (133.533, 125.05), (133.464, 124.82)], 'J1.5 -> through via'),
 ('B.Cu', 0.10, [(133.885, 125.52), (133.886, 124.163)], 'J1.6 -> through via'),
 ('B.Cu', 0.10, [(134.235, 125.52), (134.235, 125.05), (134.371, 124.787)], 'J1.7 -> through via'),
 ('B.Cu', 0.10, [(135.289, 125.52), (135.307, 123.882)], 'J1.10 -> through via'),
 # J1 bottom row: short stubs into vias right next to the pads
 ('B.Cu', 0.15, [(132.48, 127.42), (132.521, 127.81)], 'J1.14 -> through via'),
 ('B.Cu', 0.15, [(133.183, 127.42), (133.24, 127.89)], 'J1.16 -> microvia'),
 ('B.Cu', 0.15, [(133.885, 127.42), (133.91, 127.84)], 'J1.18 -> microvia'),
 ('B.Cu', 0.15, [(134.587, 127.42), (134.63, 127.855)], 'J1.20 -> microvia'),
 ('B.Cu', 0.15, [(135.289, 127.42), (135.332, 127.805)], 'J1.22 -> through via'),
 # J4 (6-pin FPC)
 ('B.Cu', 0.15, [(117.775, 123.55), (117.796, 123.046)], 'J4.1 -> through via'),
 ('B.Cu', 0.15, [(118.275, 123.55), (118.255, 123.04)], 'J4.2 -> microvia'),
 ('B.Cu', 0.15, [(119.775, 123.55), (119.827, 122.666)], 'J4.5 -> through via'),
 # J2 (2x3 board-to-board)
 ('B.Cu', 0.15, [(106.85, 125.80), (106.861, 125.473)], 'J2.2 -> through via'),
 ('B.Cu', 0.15, [(106.85, 128.58), (106.763, 128.985)], 'J2.5 -> through via'),
]
# Blind microvias confirmed in the photo at the end of a surface trace: (x, y, side)
MICROVIAS = [
 (133.24, 127.89, 'B'), (133.91, 127.84, 'B'), (134.63, 127.855, 'B'), (118.255, 123.04, 'B'),
]
