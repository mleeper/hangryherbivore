FRACTIONS = {0.25: "¼", 0.5: "½", 0.75: "¾", 0.125: "⅛", 0.33: "⅓", 0.67: "⅔"}
LABELS = {
    "clove": ("clove", "cloves"), "head": ("head", "heads"),
    "stalk": ("stalk", "stalks"), "sprig": ("sprig", "sprigs"),
    "leaf": ("leaf", "leaves"), "slice": ("slice", "slices"),
    "piece": ("piece", "pieces"),
    "block": ("block", "blocks"),
}
WHOLE_ONLY = {"clove", "sprig", "leaf", "slice", "piece"}
MULTIPLIERS = [0.5, 1, 2, 3, 4]

def fmt_number(n):
    whole, frac = int(n), round(n - int(n), 2)
    if frac == 0:
        return str(whole)
    if frac in FRACTIONS:
        return f"{whole}{FRACTIONS[frac]}" if whole else FRACTIONS[frac]
    return f"{n:.1f}".rstrip("0").rstrip(".")

def scale_qty(qty, unit, factor):
    q = qty * factor
    if unit in ("g", "ml", "kg", "l"):
        return round(q) if q >= 10 else round(q, 1)
    if unit in WHOLE_ONLY:
        return max(1, round(q))
    return max(0.5, round(q * 2) / 2)

def format_amount(qty, unit, metric=None, metric_unit=None):
    if unit in ("g", "ml", "kg", "l"):
        return f"{fmt_number(qty)}{unit}"
    if unit == "half":
        text = fmt_number(qty / 2)
    elif unit == "whole":
        text = fmt_number(qty)
    else:
        one, many = LABELS.get(unit, (unit, unit))
        text = f"{fmt_number(qty)} {one if qty == 1 else many}"
    return f"{text} ({fmt_number(metric)}{metric_unit})" if metric is not None else text

def display_variants(qty, unit, metric, metric_unit):
    out = {}
    for m in MULTIPLIERS:
        q = scale_qty(qty, unit, m)
        scaled_metric = metric * m if metric is not None else None
        out[str(m)] = format_amount(q, unit, scaled_metric, metric_unit)
    return out