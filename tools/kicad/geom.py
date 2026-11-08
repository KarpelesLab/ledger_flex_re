import math
def outline_prims(V):
    """Return list of ('line', p0, p1) / ('arc', start, mid, end) from vertex list with fillets."""
    pts = []  # expand: for normal vertices compute fillet tangent points
    n = len(V)
    def isarc(v): return v[0] == 'ARC'
    prims = []
    # resolve each vertex into (in_point, out_point, arc_or_None)
    res = []
    for i, v in enumerate(V):
        if isarc(v):
            res.append((v[1], v[3], ('arc', v[1], v[2], v[3]))); continue
        x, y, r = v
        if r <= 0:
            res.append(((x, y), (x, y), None)); continue
        # neighbours: previous out point and next in point (use raw coordinates of neighbours)
        pv = V[i - 1]; nv = V[(i + 1) % n]
        p_prev = pv[3] if isarc(pv) else pv[:2]
        p_next = nv[1] if isarc(nv) else nv[:2]
        d1 = (p_prev[0] - x, p_prev[1] - y); l1 = math.hypot(*d1); d1 = (d1[0] / l1, d1[1] / l1)
        d2 = (p_next[0] - x, p_next[1] - y); l2 = math.hypot(*d2); d2 = (d2[0] / l2, d2[1] / l2)
        ang = math.acos(max(-1, min(1, d1[0] * d2[0] + d1[1] * d2[1])))
        t = r / math.tan(ang / 2)
        a = (x + d1[0] * t, y + d1[1] * t); b = (x + d2[0] * t, y + d2[1] * t)
        bis = (d1[0] + d2[0], d1[1] + d2[1]); lb = math.hypot(*bis); bis = (bis[0] / lb, bis[1] / lb)
        dc = r / math.sin(ang / 2)
        c = (x + bis[0] * dc, y + bis[1] * dc)
        m = (c[0] - bis[0] * r, c[1] - bis[1] * r)
        res.append((a, b, ('arc', a, m, b)))
    for i in range(n):
        a, b, arc = res[i]
        if arc: prims.append(arc)
        na = res[(i + 1) % n][0]
        if math.hypot(na[0] - b[0], na[1] - b[1]) > 1e-6: prims.append(('line', b, na))
    return prims
