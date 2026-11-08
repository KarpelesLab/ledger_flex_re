import pcbnew, sys, os, string
lib = sys.argv[1]; IO = pcbnew.PCB_IO_KICAD_SEXPR()
os.makedirs(lib, exist_ok=True)
mm = pcbnew.FromMM
def V(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))
def rect(fp, layer, w, h, width):
    pts = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
    for i in range(4):
        s = pcbnew.PCB_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(layer); s.SetWidth(mm(width))
        s.SetStart(V(*pts[i])); s.SetEnd(V(*pts[(i + 1) % 4])); fp.Add(s)
def text_setup(fp, name, h):
    fp.SetFPID(pcbnew.LIB_ID('ledger_flex', name)); fp.SetReference('REF**')
    fp.Reference().SetLayer(pcbnew.F_SilkS); fp.Reference().SetPosition(V(0, -h/2 - 0.6))
    fp.Value().SetLayer(pcbnew.F_Fab); fp.Value().SetPosition(V(0, h/2 + 0.6)); fp.Value().SetText(name)
    for t in (fp.Reference(), fp.Value()):
        t.SetTextSize(V(0.4, 0.4)); t.SetTextThickness(mm(0.06))
def wlcsp(name, w, h, cols, rows, pitch, pad, desc):
    fp = pcbnew.FOOTPRINT(None)
    text_setup(fp, name, h); fp.SetLibDescription(desc); fp.SetAttributes(pcbnew.FP_SMD)
    x0 = -(cols - 1) * pitch / 2; y0 = -(rows - 1) * pitch / 2
    letters = [c for c in string.ascii_uppercase if c not in 'IOQSXZ']
    for r in range(rows):
        for c in range(cols):
            p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            p.SetSize(V(pad, pad)); p.SetLayerSet(p.SMDMask()); p.SetNumber(f'{letters[r]}{c + 1}')
            p.SetPosition(V(x0 + c * pitch, y0 + r * pitch)); fp.Add(p)
    rect(fp, pcbnew.F_Fab, w, h, 0.05)
    rect(fp, pcbnew.F_CrtYd, w + 0.4, h + 0.4, 0.05)
    # silk corner mark at A1
    s = pcbnew.PCB_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_CIRCLE); s.SetLayer(pcbnew.F_SilkS); s.SetWidth(mm(0.1))
    s.SetCenter(V(-w/2 - 0.25, -h/2 - 0.25)); s.SetEnd(V(-w/2 - 0.2, -h/2 - 0.25)); fp.Add(s)
    IO.FootprintSave(lib, fp)
wlcsp('WLCSP-24_2.56x1.81mm_Layout6x4_P0.4mm', 2.56, 1.81, 6, 4, 0.4, 0.22,
      'Secure element WLCSP-24 (6x4, 0.4mm pitch), body 2.56x1.81mm measured. Ball A1 orientation not yet confirmed.')
wlcsp('WLCSP-36_3.2x3.2mm_Layout6x6_P0.5mm', 3.2, 3.2, 6, 6, 0.5, 0.25,
      'ST25R3916 WLCSP-36 (6x6, 0.5mm pitch), body ~3.2x3.2mm measured. Ball A1 orientation not yet confirmed.')
for drill, pad in ((3.0, 4.2), (3.0, 4.0), (1.5, 2.75)):
    fp = pcbnew.FOOTPRINT(None); name = f'MountingHole_{drill}mm_Pad{pad}'
    text_setup(fp, name, pad); fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_EXCLUDE_FROM_BOM)
    p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_PTH); p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    p.SetSize(V(pad, pad)); p.SetDrillSize(V(drill, drill)); p.SetLayerSet(pcbnew.PAD.PTHMask()); p.SetNumber('1'); fp.Add(p)
    s = pcbnew.PCB_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_CIRCLE); s.SetLayer(pcbnew.F_CrtYd); s.SetWidth(mm(0.05))
    s.SetCenter(V(0, 0)); s.SetEnd(V(pad / 2 + 0.25, 0)); fp.Add(s)
    IO.FootprintSave(lib, fp)
print(sorted(os.listdir(lib)))
fp = pcbnew.FOOTPRINT(None); name = 'TestPad_D1.0mm'
text_setup(fp, name, 1.0); fp.SetAttributes(pcbnew.FP_SMD | pcbnew.FP_EXCLUDE_FROM_BOM)
p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
p.SetSize(V(1.0, 1.0)); p.SetLayerSet(p.SMDMask()); p.SetNumber('1'); fp.Add(p)
IO.FootprintSave(lib, fp)

# ---- connectors measured on the bottom side. Pads are given in board-frame coordinates
# relative to the footprint origin as seen from the TOP (x right, y down); y is negated
# here because flipping to B.Cu mirrors the footprint in y. Pin numbering is arbitrary
# (row by row, left to right as seen from the top), not the manufacturer's.
def conn(name, desc, sig, mech, body):
    fp = pcbnew.FOOTPRINT(None); text_setup(fp, name, body[1]); fp.SetLibDescription(desc)
    fp.SetAttributes(pcbnew.FP_SMD)
    for num, (x, y, w, h) in enumerate(sig, 1):
        p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetShape(pcbnew.PAD_SHAPE_ROUNDRECT)
        p.SetRoundRectRadiusRatio(0.25); p.SetSize(V(w, h)); p.SetLayerSet(p.SMDMask())
        p.SetNumber(str(num)); p.SetPosition(V(x, -y)); fp.Add(p)
    for (x, y, w, h) in mech:
        p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetShape(pcbnew.PAD_SHAPE_RECT)
        p.SetSize(V(w, h)); p.SetLayerSet(p.SMDMask()); p.SetNumber('MP'); p.SetPosition(V(x, -y)); fp.Add(p)
    rect(fp, pcbnew.F_Fab, body[0], body[1], 0.05)
    rect(fp, pcbnew.F_CrtYd, body[0] + 0.3, body[1] + 0.3, 0.05)
    IO.FootprintSave(lib, fp)
def rowpads(n, pitch, y, w, h):
    return [((k - (n - 1) / 2) * pitch, y, w, h) for k in range(n)]
conn('BtB_2x12_P0.35mm_measured', 'Board-to-board 2x12, 0.35 mm pitch (Hirose BM28-style), measured from photos',
     rowpads(12, 0.351, -0.95, 0.20, 0.55) + rowpads(12, 0.351, 0.95, 0.20, 0.55),
     [(-3.27, 0, 0.30, 0.70), (3.27, 0, 0.30, 0.70)] + [(sx * 2.61, sy * 1.02, 0.40, 0.30) for sx in (-1, 1) for sy in (-1, 1)], (6.6, 2.3))
conn('BtB_2x3_P0.4mm_A_measured', 'Board-to-board 2x3, 0.4 mm pitch, rows 1.88 mm apart, measured from photos',
     rowpads(3, 0.40, -1.39, 0.22, 0.40) + rowpads(3, 0.40, 1.39, 0.22, 0.40), [(sx * 1.10, sy * 1.39, 0.40, 0.35) for sx in (-1, 1) for sy in (-1, 1)], (3.6, 3.0))
conn('BtB_2x3_P0.4mm_B_measured', 'Board-to-board 2x3, 0.4 mm pitch, tails 2.71 mm apart, measured from photos',
     [(-1.355, (k - 1) * 0.40, 0.45, 0.22) for k in range(3)] + [(1.355, (k - 1) * 0.40, 0.45, 0.22) for k in range(3)],
     [(-1.18, -1.20, 0.35, 0.65), (1.16, -1.24, 0.35, 0.65), (-1.17, 1.20, 0.35, 0.65), (1.18, 1.16, 0.35, 0.65)], (3.0, 3.2))
conn('FPC_1x06_P0.5mm_measured', 'FPC connector, 6 contacts, 0.5 mm pitch, flip lock, measured from photos',
     rowpads(6, 0.50, 0, 0.30, 0.70), [(-2.30, 2.65, 0.40, 0.90), (2.30, 2.65, 0.40, 0.90)], (5.0, 3.4))
conn('FPC_1x04_P0.5mm_measured', 'FPC connector, 4 contacts, 0.5 mm pitch, flip lock, measured from photos',
     rowpads(4, 0.50, 0, 0.30, 0.70), [(-1.75, 2.60, 0.30, 0.90), (1.75, 2.60, 0.30, 0.90)], (4.0, 3.2))

# ---------------------------------------------------------------------------
# Simple 3D bodies (VRML boxes) so every custom footprint renders at its measured
# size. KiCad VRML units are 0.1 inch. Boxes are (x0, y0, x1, y1, z0, z1, colour)
# in footprint millimetres, y down, as seen from the side the part is mounted on.
MODELDIR = os.path.join(os.path.dirname(os.path.abspath(lib)), '3d')
BLACK, DGREY, LGREY, SILVER, WHITE, BEIGE, GOLD, COPPER = (
    (.08, .08, .08), (.25, .25, .27), (.6, .6, .6), (.82, .82, .84), (.93, .92, .88), (.72, .6, .42), (.85, .7, .3), (.6, .35, .2))
def wrl(name, boxes):
    os.makedirs(MODELDIR, exist_ok=True); f = 1 / 2.54
    out = ['#VRML V2.0 utf8']
    for x0, y0, x1, y1, z0, z1, c in boxes:
        X0, X1, Y0, Y1, Z0, Z1 = x0 * f, x1 * f, -y1 * f, -y0 * f, z0 * f, z1 * f
        pts = [(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y1, Z0), (X0, Y1, Z0), (X0, Y0, Z1), (X1, Y0, Z1), (X1, Y1, Z1), (X0, Y1, Z1)]
        out.append('Shape { appearance Appearance { material Material { diffuseColor %.3f %.3f %.3f specularColor .25 .25 .25 shininess .3 } }' % c)
        out.append(' geometry IndexedFaceSet { solid FALSE coord Coordinate { point [ %s ] }' % ', '.join('%.5f %.5f %.5f' % p for p in pts))
        out.append('  coordIndex [ 0 3 2 1 -1 4 5 6 7 -1 0 1 5 4 -1 1 2 6 5 -1 2 3 7 6 -1 3 0 4 7 -1 ] } }')
    open(os.path.join(MODELDIR, name + '.wrl'), 'w').write('\n'.join(out) + '\n')
def add_model(fp, name, boxes):
    wrl(name, boxes)
    m = pcbnew.FP_3DMODEL(); m.m_Filename = '${KIPRJMOD}/3d/' + name + '.wrl'; fp.Models().append(m)
def body_box(w, h, z, c, cx=0, cy=0):
    return [(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 0, z, c)]
def chip_boxes(L, W, H, c, cap=SILVER, capL=None):
    capL = capL or L * 0.2
    return [(-L / 2, -W / 2, -L / 2 + capL, W / 2, 0, H, cap), (L / 2 - capL, -W / 2, L / 2, W / 2, 0, H, cap),
            (-L / 2 + capL, -W / 2, L / 2 - capL, W / 2, 0.01, H, c)]
def custom(name, desc, pads, body, height, colour, boxes=None, mirror=False, smd=True, pth=()):
    """pads: (num, x, y, w, h, shape) in top-view mm; body: (w, h[, cx, cy]).
    mirror=True for bottom-side parts: stored with y negated (see conn())."""
    s = -1 if mirror else 1
    fp = pcbnew.FOOTPRINT(None); text_setup(fp, name, body[1]); fp.SetLibDescription(desc)
    fp.SetAttributes(pcbnew.FP_SMD if smd else pcbnew.FP_THROUGH_HOLE)
    for num, x, y, w, h, shape in pads:
        p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        p.SetShape({'rect': pcbnew.PAD_SHAPE_RECT, 'round': pcbnew.PAD_SHAPE_ROUNDRECT, 'circle': pcbnew.PAD_SHAPE_CIRCLE}[shape])
        if shape == 'round': p.SetRoundRectRadiusRatio(0.25)
        p.SetSize(V(w, h)); p.SetLayerSet(p.SMDMask()); p.SetNumber(str(num)); p.SetPosition(V(x, s * y)); fp.Add(p)
    for num, x, y, w, h, dw, dh in pth:  # oval plated slots
        p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_PTH); p.SetShape(pcbnew.PAD_SHAPE_OVAL)
        p.SetSize(V(w, h)); p.SetDrillShape(pcbnew.PAD_DRILL_SHAPE_OBLONG); p.SetDrillSize(V(dw, dh))
        p.SetLayerSet(pcbnew.PAD.PTHMask()); p.SetNumber(str(num)); p.SetPosition(V(x, s * y)); fp.Add(p)
    bw, bh = body[0], body[1]; cx, cy = (body[2], body[3]) if len(body) > 2 else (0, 0)
    for layer, g in ((pcbnew.F_Fab, 0), (pcbnew.F_CrtYd, 0.15)):
        pts = [(cx - bw / 2 - g, cy - bh / 2 - g), (cx + bw / 2 + g, cy - bh / 2 - g), (cx + bw / 2 + g, cy + bh / 2 + g), (cx - bw / 2 - g, cy + bh / 2 + g)]
        for i in range(4):
            sh = pcbnew.PCB_SHAPE(fp); sh.SetShape(pcbnew.SHAPE_T_SEGMENT); sh.SetLayer(layer); sh.SetWidth(mm(0.05))
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 4]
            sh.SetStart(V(ax, s * ay)); sh.SetEnd(V(bx, s * by)); fp.Add(sh)
    boxes = boxes if boxes is not None else body_box(bw, bh, height, colour, cx, cy)
    if mirror: boxes = [(x0, -y1, x1, -y0, z0, z1, c) for x0, y0, x1, y1, z0, z1, c in boxes]
    if boxes: add_model(fp, name, boxes)
    IO.FootprintSave(lib, fp)
    return fp
def chip2(name, desc, L, W, H, padL, padW, pitch, colour, cap=SILVER, capL=None):
    custom(name, desc, [(1, -pitch / 2, 0, padL, padW, 'round'), (2, pitch / 2, 0, padL, padW, 'round')],
           (L, W), H, colour, chip_boxes(L, W, H, colour, cap, capL))

# Existing measured footprints get bodies too (re-saved with a model).
def remodel(name, boxes):
    fp = IO.FootprintLoad(lib, name); fp.Models().clear(); add_model(fp, name, boxes); IO.FootprintSave(lib, fp)
remodel('WLCSP-24_2.56x1.81mm_Layout6x4_P0.4mm', [(-1.28, -0.905, 1.28, 0.905, 0.15, 0.5, DGREY)])
remodel('WLCSP-36_3.2x3.2mm_Layout6x6_P0.5mm', [(-1.6, -1.6, 1.6, 1.6, 0.15, 0.55, BLACK)])
remodel('BtB_2x12_P0.35mm_measured', [(-3.3, -1.15, 3.3, 1.15, 0, 0.6, DGREY)])
remodel('BtB_2x3_P0.4mm_A_measured', [(-1.8, -1.5, 1.8, 1.5, 0, 0.6, DGREY)])
remodel('BtB_2x3_P0.4mm_B_measured', [(-1.5, -1.6, 1.5, 1.6, 0, 0.6, DGREY)])
remodel('FPC_1x06_P0.5mm_measured', [(-2.5, -1.7, 2.5, 1.7, 0, 0.9, BLACK)])
remodel('FPC_1x04_P0.5mm_measured', [(-2.0, -1.6, 2.0, 1.6, 0, 0.9, BLACK)])

# ---- two-terminal parts whose body or pads differ from the standard library sizes
chip2('R_0603_1608Metric_LargePads', '0603 resistor (body 1.6x0.8, measured) on oversized 2.55x1.05 pad pair',
      1.6, 0.8, 0.45, 0.75, 1.05, 1.80, BLACK)
chip2('D_1.8x1.05mm_EndTerminals', 'Diode, flat package 1.8x1.05 mm with end terminals (marking d), measured',
      1.8, 1.05, 0.6, 0.55, 0.95, 1.40, BLACK, capL=0.15)
chip2('D_1.0x0.6mm', 'Two-terminal DFN 1.0x0.6 mm (SOD-882 class), terminals 0.5 mm apart (X-ray), measured',
      1.0, 0.6, 0.4, 0.30, 0.55, 0.50, BLACK, cap=DGREY, capL=0.15)
chip2('L_2.55x1.05mm_WireWound', 'Wire-wound chip inductor 2.55x1.05 mm, measured',
      2.55, 1.05, 0.9, 0.60, 1.00, 1.95, COPPER, capL=0.35)
chip2('L_2.5x1.45mm', 'Chip inductor 2.5x1.45 mm (light grey body), measured',
      2.5, 1.45, 1.0, 0.60, 1.40, 1.90, LGREY, capL=0.35)
chip2('2T_2.2x1.4mm_MetalLid', 'Two-terminal part 2.2x1.4 mm, grey metal lid with dot, terminals at the ends (X-ray), measured',
      2.2, 1.4, 0.8, 0.60, 1.30, 1.70, LGREY, cap=LGREY, capL=0.3)

# ---- ICs and other packages measured from photos and X-ray (top view, pin 1 top-left)
wlcsp('BGA-25_2.15x2.1mm_Layout5x5_P0.4mm', 2.15, 2.1, 5, 5, 0.4, 0.22,
      'BGA/WLCSP-25 (5x5, 0.4 mm pitch, balls located in X-ray), body 2.15x2.1 mm measured, marking 9420')
remodel('BGA-25_2.15x2.1mm_Layout5x5_P0.4mm', [(-1.075, -1.05, 1.075, 1.05, 0.1, 0.65, BLACK)])
custom('DFN-6_2.1x1.45mm_P0.4mm', 'Leadless 6-pad package 2.1x1.45 mm (ST, marking 022), pads from X-ray',
       [(i + 1, -0.62, (i - 1) * 0.4, 0.35, 0.22, 'round') for i in range(3)] + [(6 - i, 0.62, (i - 1) * 0.4, 0.35, 0.22, 'round') for i in range(3)],
       (2.1, 1.45), 0.55, BLACK)
custom('DFN-3_0.7x0.7mm', '3-pad leadless package 0.7x0.7 mm (two small pads, one large), pads from X-ray',
       [(1, -0.2, -0.13, 0.22, 0.18, 'rect'), (2, -0.2, 0.15, 0.22, 0.18, 'rect'), (3, 0.17, 0.01, 0.22, 0.45, 'rect')],
       (0.7, 0.7), 0.4, BLACK)
custom('WLCSP-4_1.2x1.15mm', '4-pad die-size package 1.2x1.15 mm (bare die back visible), measured',
       [(n, x, y, 0.25, 0.25, 'circle') for n, (x, y) in enumerate(((-0.55, -0.32), (0.55, -0.32), (-0.55, 0.32), (0.55, 0.32)), 1)],
       (1.2, 1.15), 0.45, DGREY)
custom('RF_Ceramic_2.05x1.25mm_8T', 'Ceramic RF part (filter/balun) 2.05x1.25 mm, 8 terminals, measured',
       [(n + 1, x, -0.95, 0.32, 0.65, 'rect') for n, x in enumerate((-0.55, 0, 0.55))] + [(4, 1.3, 0, 0.65, 0.3, 'rect')] +
       [(7 - n, x, 0.95, 0.32, 0.65, 'rect') for n, x in enumerate((-0.55, 0, 0.55))] + [(8, -1.3, 0, 0.65, 0.3, 'rect')],
       (2.05, 1.25), 0.6, WHITE)
custom('DFN-6-1EP_1.85x1.95mm_P0.5mm', 'DFN-6 with exposed pad, 1.85x1.95 mm, 0.5 mm pitch, pins on top and bottom edges (marking VD1)',
       [(n + 1, x, -0.88, 0.25, 0.45, 'rect') for n, x in enumerate((-0.5, 0, 0.5))] +
       [(6 - n, x, 0.88, 0.25, 0.45, 'rect') for n, x in enumerate((-0.5, 0, 0.5))] + [(7, 0, 0, 1.6, 1.0, 'rect')],
       (1.85, 1.95), 0.75, BLACK)
custom('DFN-4_0.65x0.67mm', 'Leadless 4-pad package 0.65x0.67 mm, pads approximate', 
       [(n, x, y, 0.18, 0.18, 'rect') for n, (x, y) in enumerate(((-0.18, -0.18), (0.18, -0.18), (0.18, 0.18), (-0.18, 0.18)), 1)],
       (0.65, 0.67), 0.35, BLACK)
custom('DFN-6_0.65x0.8mm', 'Leadless 6-pad package 0.65x0.8 mm, pads approximate',
       [(i + 1, -0.2, (i - 1) * 0.25, 0.15, 0.15, 'rect') for i in range(3)] + [(6 - i, 0.2, (i - 1) * 0.25, 0.15, 0.15, 'rect') for i in range(3)],
       (0.65, 0.8), 0.35, BLACK)
custom('LGA-4_0.48x0.65mm_PadsOutside', '4-pad part, body 0.48x0.65 mm with pads at the corners just outside the body, measured',
       [(n, x, y, 0.22, 0.22, 'rect') for n, (x, y) in enumerate(((-0.28, -0.32), (0.28, -0.32), (0.28, 0.32), (-0.28, 0.32)), 1)],
       (0.48, 0.65), 0.35, LGREY)
# bottom-side parts (mirror=True)
custom('SON-6-2T_2.05x1.95mm_P0.5mm', '2x2 mm package, 3 pins per side at 0.5 mm plus top/bottom tabs (marking IDC 02), measured',
       [(i + 1, -1.0, (i - 1) * 0.5, 0.35, 0.25, 'rect') for i in range(3)] + [(6 - i, 1.0, (i - 1) * 0.5, 0.35, 0.25, 'rect') for i in range(3)] +
       [(7, 0, -0.98, 1.1, 0.25, 'rect'), (8, 0, 0.98, 1.1, 0.25, 'rect')],
       (2.05, 1.95), 0.6, BLACK, mirror=True)
custom('DFN-3_0.83x1.17mm', '3-pad leadless package 0.83x1.17 mm (two small pads, one wide), pads from X-ray',
       [(1, -0.18, -0.33, 0.25, 0.3, 'rect'), (2, 0.18, -0.33, 0.25, 0.3, 'rect'), (3, 0, 0.36, 0.55, 0.3, 'rect')],
       (0.83, 1.17), 0.4, BLACK, mirror=True)
custom('BtB_2x3_P0.35mm_C_measured', 'Board-to-board 2x3, ~0.36 mm pitch, pad columns 1.63 mm apart, measured from photo and X-ray',
       [(i + 1, -0.815, (i - 1) * 0.365, 0.8, 0.2, 'round') for i in range(3)] + [(i + 4, 0.815, (i - 1) * 0.365, 0.8, 0.2, 'round') for i in range(3)] +
       [('MP', sx * 0.95, sy * 1.15, 0.5, 0.6, 'rect') for sx in (-1, 1) for sy in (-1, 1)],
       (2.4, 2.95), 0.6, DGREY, mirror=True)
custom('Pads_2x2_0.65x0.45mm_Unpopulated', 'Four exposed gold pads (unpopulated footprint), measured',
       [(n, x, y, 0.65, 0.45, 'rect') for n, (x, y) in enumerate(((-0.575, -0.6), (0.575, -0.6), (0.575, 0.6), (-0.575, 0.6)), 1)],
       (1.8, 1.65), 0, BLACK, boxes=[], mirror=True)
for d in (1.1, 1.5):
    custom(f'TestPad_D{d}mm', f'Round exposed test pad, {d} mm', [(1, 0, 0, d, d, 'circle')], (d, d), 0, BLACK, boxes=[])
custom('TestPad_Square0.6mm', 'Square exposed pad 0.6 mm', [(1, 0, 0, 0.6, 0.6, 'rect')], (0.6, 0.6), 0, BLACK, boxes=[])
# USB-C receptacle, mid-mount (body sits in a board cutout). Origin at the centre of the
# SMD pad row. 12 pad positions (16-pin USB 2.0 layout); slot legs located in the X-ray.
usb_y = [-3.2, -2.4, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.4, 3.2]
custom('USB_C_Receptacle_MidMount_16P_measured', 'USB-C receptacle, mid-mount in board cutout, 16-pin (12 pad positions), measured from X-ray',
       [(i + 1, 0, y, 1.1, 0.6 if abs(y) > 2 else 0.3, 'round') for i, y in enumerate(usb_y)],
       (9.1, 9.1, -2.8, -0.28), 1.3, BLACK,
       boxes=[(-7.35, -4.83, 1.75, 4.27, -1.7, 1.3, BLACK),
              (-6.35, -6.43, 1.15, -4.83, 0, 0.25, BLACK), (-6.35, 4.27, 1.15, 6.27, 0, 0.25, BLACK),
              (-6.35, -6.43, 1.15, -4.83, -1.05, -0.8, BLACK), (-6.35, 4.27, 1.15, 6.27, -1.05, -0.8, BLACK)],
       smd=False, pth=[('S1', -5.11, -5.88, 1.9, 0.9, 1.5, 0.5), ('S2', -0.88, -5.88, 1.9, 0.9, 1.5, 0.5),
                       ('S3', -5.11, 5.34, 1.9, 0.9, 1.5, 0.5), ('S4', -0.88, 5.34, 1.9, 0.9, 1.5, 0.5)])
wrl('Crystal_2.0x1.2mm', [(-1.0, -0.6, 1.0, 0.6, 0, 0.12, BEIGE), (-0.95, -0.55, 0.95, 0.55, 0.12, 0.55, SILVER)])  # substitute model for the library 2012 crystal
print('custom footprints done')
