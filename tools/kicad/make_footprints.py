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
