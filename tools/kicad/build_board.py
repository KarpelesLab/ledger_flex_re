import sys, os, base64, uuid, re
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from outline_def import V, HOLES
from geom import outline_prims
out = sys.argv[1]; refdir = sys.argv[2]
mm = pcbnew.FromMM
def P(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))
b = pcbnew.BOARD()
b.SetCopperLayerCount(4)
ds = b.GetDesignSettings()
ds.SetBoardThickness(mm(0.8))
# HDI-scale limits matching the measured geometry (0.2/0.4 mm vias, ~0.1 mm tracks)
ds.m_TrackMinWidth = mm(0.08); ds.m_ViasMinSize = mm(0.35); ds.m_MinThroughDrill = mm(0.15)
ds.m_ViasMinAnnularWidth = mm(0.075); ds.m_HoleClearance = mm(0.1); ds.m_HoleToHoleMin = mm(0.15)
ds.m_CopperEdgeClearance = mm(0.15); ds.m_MinClearance = mm(0.075)
# name user layers used for references
b.SetLayerName(pcbnew.User_1, 'Ref.TopPhoto')
b.SetLayerName(pcbnew.User_2, 'Ref.BottomPhoto')
b.SetLayerName(pcbnew.User_3, 'Ref.XRay')
for pr in outline_prims(V):
    s = pcbnew.PCB_SHAPE(b)
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.05))
    if pr[0] == 'line':
        s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(P(*pr[1])); s.SetEnd(P(*pr[2]))
    else:
        s.SetShape(pcbnew.SHAPE_T_ARC); s.SetArcGeometry(P(*pr[1]), P(*pr[2]), P(*pr[3]))
    b.Add(s)
IO = pcbnew.PCB_IO_KICAD_SEXPR()
LIBS = {'ledger_flex': os.path.join(os.path.dirname(out), 'ledger_flex.pretty'),
        'Package_DFN_QFN': '/usr/share/kicad/footprints/Package_DFN_QFN.pretty'}
def place(lib, name, ref, value, x, y, rot=0, side='F', hide_text=False):
    fp = IO.FootprintLoad(LIBS[lib], name)
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    fp.SetReference(ref); fp.SetValue(value)
    b.Add(fp)
    if side == 'B': fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    fp.SetOrientationDegrees(rot); fp.SetPosition(P(x, y))
    if hide_text: fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    return fp
for name, x, y, drill, pad in HOLES:
    place('ledger_flex', f'MountingHole_{drill}mm_Pad{pad}', name, f'MountingHole_{drill}mm', x, y, hide_text=True)
from parts import PARTS
for p in PARTS: place(*p)
import json
for x, y, *_ in json.load(open(os.path.join(os.path.dirname(__file__), 'vias_confirmed.json'))):
    v = pcbnew.PCB_VIA(b); v.SetPosition(P(x, y)); v.SetWidth(mm(0.4)); v.SetDrill(mm(0.2))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); b.Add(v)
from tracks_manual import TRACKS
LAY = {'F.Cu': pcbnew.F_Cu, 'B.Cu': pcbnew.B_Cu}
for layer, w, pts, note in TRACKS:
    for a, c in zip(pts[:-1], pts[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(P(*a)); t.SetEnd(P(*c)); t.SetWidth(mm(w)); t.SetLayer(LAY[layer]); b.Add(t)
pcbnew.SaveBoard(out, b)
# --- insert reference images
def img_block(path, layer, cx, cy):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    lines = [data[i:i + 76] for i in range(0, len(data), 76)]
    body = '\n'.join(f'\t\t\t"{l}"' for l in lines)
    return (f'\t(image\n\t\t(at {cx} {cy})\n\t\t(layer "{layer}")\n\t\t(scale 1)\n\t\t(locked yes)\n'
            f'\t\t(uuid "{uuid.uuid4()}")\n\t\t(data\n{body}\n\t\t)\n\t)\n')
txt = open(out).read().rstrip()
assert txt.endswith(')')
cx, cy = (100 + 154) / 2, (98 + 134) / 2
blocks = ''.join(img_block(os.path.join(refdir, f), l, cx, cy) for f, l in
                 (('ref_xray.png', 'User.3'), ('ref_bottom.png', 'User.2'), ('ref_top.png', 'User.1')))
open(out, 'w').write(txt[:-1] + blocks + ')\n')
print('saved', out, os.path.getsize(out))
