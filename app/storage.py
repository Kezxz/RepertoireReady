import os, csv
from typing import List, Dict, Tuple
import piece_logic as tpl
import setlist_logic as sl

# file locations
PIECES_CSV = os.path.join("data", "piece_library.csv")
SETLISTS_CSV = os.path.join("data", "setlist_library.csv")

PIECE_HEADER_WRITE = ["piece_id","title","composer","genre","readiness_status","user_id","created","updated"]
SETLIST_HEADER_WRITE = ["id","title","date","location","user_id","piece_ids"]  # piece_ids joined by ";"

def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

# ----------- Pieces ----------- #

def load_pieces(path: str = PIECES_CSV) -> List[tpl.Piece]:
    _ensure_parent(path)
    pieces: List[tpl.Piece] = []
    if not os.path.exists(path):
        # create empty file
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(PIECE_HEADER_WRITE)
        return pieces

    with open(path, newline="", encoding="utf-8-sig", errors="ignore") as f:
        rd = csv.DictReader(f)
        # tolerate semicolon CSV
        if rd.fieldnames and len(rd.fieldnames) == 1 and ";" in rd.fieldnames[0]:
            f.seek(0)
            rd = csv.DictReader(f, delimiter=";")
        for r in rd:
            try:
                pid = int((r.get("piece_id") or "0").strip())
            except ValueError:
                continue
            p = tpl.Piece(
                piece_id=pid,
                title=r.get("title","") or "",
                composer=r.get("composer","") or "",
                genre=r.get("genre","") or "",
                readiness_status=(r.get("readiness_status","learning") or "learning").strip().lower(),
                user_id=int((r.get("user_id") or "0").strip() or 0),
            )
            p.created = (r.get("created") or "").strip() or None
            p.updated = (r.get("updated") or "").strip() or None
            pieces.append(p)
    return pieces

def save_pieces(pieces: List[tpl.Piece], path: str = PIECES_CSV) -> None:
    _ensure_parent(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(PIECE_HEADER_WRITE)
        for p in pieces:
            wr.writerow([
                p.piece_id,
                p.title,
                p.composer,
                p.genre,
                (p.readiness_status or "learning"),
                p.user_id,
                p.created if getattr(p, "created", None) else "",
                p.updated if getattr(p, "updated", None) else "",
            ])

# ----------- Setlists ----------- #

def load_setlists(path: str = SETLISTS_CSV) -> Tuple[Dict[int, sl.Performance], List[sl.Setlist_Item]]:
    _ensure_parent(path)
    performances: Dict[int, sl.Performance] = {}
    items: List[sl.Setlist_Item] = []

    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(SETLIST_HEADER_WRITE)
        return performances, items

    with open(path, newline="", encoding="utf-8-sig", errors="ignore") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames and len(rd.fieldnames) == 1 and ";" in rd.fieldnames[0]:
            f.seek(0)
            rd = csv.DictReader(f, delimiter=";")
        for r in rd:
            try:
                pid = int((r.get("id") or "0").strip())
            except ValueError:
                continue
            perf = sl.Performance(
                pid,
                r.get("title","") or "",
                r.get("date","") or "",
                r.get("location","") or "",
                int((r.get("user_id") or "0").strip() or 0),
            )
            performances[pid] = perf

            ids = [int(x) for x in (r.get("piece_ids","").split(";")) if x.strip()]
            for idx, piece_id in enumerate(ids, start=1):
                items.append(sl.Setlist_Item(len(items)+1, pid, piece_id, idx))

    return performances, items

def save_setlists(performances: Dict[int, sl.Performance], items: List[sl.Setlist_Item], path: str = SETLISTS_CSV) -> None:
    _ensure_parent(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(SETLIST_HEADER_WRITE)
        for pid, perf in performances.items():
            # inline items_for(pid) to keep main simpler elsewhere
            ordered = sorted([it for it in items if it.performance_id == pid], key=lambda t: t.order_index)
            piece_ids = [str(it.piece_id) for it in ordered]
            wr.writerow([pid, perf.title, perf.date, perf.location, perf.user_id, ";".join(piece_ids)])