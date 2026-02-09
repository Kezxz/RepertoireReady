from datetime import date
import csv
import os

import piece_logic as tpl

READINESS = ["learning", "rehearsing", "performance-ready"]

_LIB = tpl.PieceLibrary()


# ----------- Helpers (IDs, lookups, resolution) ----------- #

def _next_piece_id() -> int:
    return max([p.piece_id for p in _LIB.pieces], default=0) + 1

# small, user-friendly ID
def _next_simple_piece_id() -> int:
    used = {getattr(p, "simple_id", 0) for p in _LIB.pieces if getattr(p, "simple_id", 0)}
    i = 1
    while i in used:
        i += 1
    return i

# check by internal piece_id
def exists_piece_id(pid: int) -> bool:
    return any(p.piece_id == pid for p in _LIB.pieces)

# accepts: simple id, internal id, or partial title.
# returns the internal piece_id
def _resolve_piece_ref(ref: str) -> int | None:
    s = (ref or "").strip()
    if not s:
        print("No reference provided.")
        return None

    # try integers first (prefer simple_id match, then internal id)
    if s.isdigit():
        num = int(s)
        by_simple = next((p for p in _LIB.pieces if getattr(p, "simple_id", None) == num), None)
        if by_simple:
            return by_simple.piece_id
        by_id = next((p for p in _LIB.pieces if p.piece_id == num), None)
        if by_id:
            return by_id.piece_id

    # partial title match (case-insensitive)
    matches = [p for p in _LIB.pieces if s.lower() in (p.title or "").lower()]
    if not matches:
        print("No piece matched that reference.")
        return None
    if len(matches) == 1:
        return matches[0].piece_id

    # multiple: disambiguate by simple_id
    print("Multiple matches:")
    for p in matches:
        si = getattr(p, "simple_id", "?")
        print(f"- {si}: {p.title} ({p.composer})")
    pick = input("Choose simple id: ").strip()
    if pick.isdigit():
        return _resolve_piece_ref(pick)
    return None


# ---------- CSV persistence for teammate model ---------- #

PIECES_CSV = "pieces.csv"
PIECE_HEADER = ["piece_id", "simple_id", "title", "composer", "genre",
                "readiness_status", "user_id", "created", "updated"]

# load pieces into library
def load_from_csv(path: str = PIECES_CSV) -> None:
    _LIB.pieces.clear()
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(PIECE_HEADER)
        return

    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        for r in rd:
            try:
                pid = int(r.get("piece_id") or 0)
            except ValueError:
                continue

            p = tpl.Piece(
                piece_id=pid,
                title=r.get("title", ""),
                composer=r.get("composer", ""),
                genre=r.get("genre", ""),
                readiness_status=(r.get("readiness_status", "learning") or "learning").strip().lower(),
                user_id=int(r.get("user_id") or 0),
            )
            # keep what's in CSV
            p.created = r.get("created") or None
            p.updated = r.get("updated") or None
            si_raw = r.get("simple_id")
            p.simple_id = int(si_raw) if (si_raw and si_raw.isdigit()) else 0

            # Append directly to library to avoid add_piece() resetting dates
            _LIB.pieces.append(p)

    # Backfill simple_id for any rows missing it
    for p in _LIB.pieces:
        if not getattr(p, "simple_id", 0):
            p.simple_id = _next_simple_piece_id()

def save_to_csv(path: str = PIECES_CSV) -> None:
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(PIECE_HEADER)
        for p in _LIB.pieces:
            wr.writerow([
                p.piece_id,
                getattr(p, "simple_id", 0),
                p.title,
                p.composer,
                p.genre,
                (p.readiness_status or "learning"),
                p.user_id,
                p.created if getattr(p, "created", None) else "",
                p.updated if getattr(p, "updated", None) else "",
            ])


# ----------- CLI-facing functions ----------- #

def _fmt_piece(p: tpl.Piece) -> str:
    si = getattr(p, "simple_id", "?")
    base = f"#{si} {p.title}: {p.composer}, {p.genre}, {p.readiness_status}"
    if getattr(p, "updated", None):
        return f"{base}, {p.created}, {p.updated}"
    return f"{base}, {p.created}"

def list_pieces() -> None:
    if not _LIB.pieces:
        print("No pieces yet.")
        return
    for p in _LIB.pieces:
        print("-", _fmt_piece(p))

def add_piece() -> None:
    title = input("Title: ").strip()
    if not title:
        print("Title is required.")
        return
    composer = input("Composer: ").strip()
    genre = input("Genre/Key: ").strip()
    print(f"Readiness options: {READINESS}")
    r = (input("Readiness [learning]: ").strip().lower() or "learning")
    if r not in READINESS:
        r = "learning"

    p = tpl.Piece(
        piece_id=_next_piece_id(),
        title=title,
        composer=composer,
        genre=genre,
        readiness_status=r,
        user_id=0,
    )

    _LIB.add_piece(p)
    # assign simple id after adding to library
    p.simple_id = _next_simple_piece_id()
    print(f"Added as #{p.simple_id}.")

def edit_piece() -> None:
    ref = input("Piece (simple id, internal id, or partial title): ").strip()
    pid = _resolve_piece_ref(ref)
    if pid is None:
        return

    # find current record
    cur = next((x for x in _LIB.pieces if x.piece_id == pid), None)
    if not cur:
        print("Not found.")
        return

    title = input(f"Title [{cur.title}]: ").strip() or cur.title
    composer = input(f"Composer [{cur.composer}]: ").strip() or cur.composer
    genre = input(f"Genre/Key [{cur.genre}]: ").strip() or cur.genre
    r = input(f"Readiness {READINESS} [{cur.readiness_status}]: ").strip().lower() or cur.readiness_status
    if r not in READINESS:
        r = cur.readiness_status

    _LIB.edit_piece(pid, title, composer, genre, r)
    print("Updated.")

def delete_piece() -> int:
    ref = input("Piece to delete (simple id, internal id, or partial title): ").strip()
    pid = _resolve_piece_ref(ref)
    if pid is None:
        return -1
    ok = _LIB.delete_piece(pid)
    print("Deleted." if ok else "Not found.")
    return pid if ok else -1

def filter_by_readiness() -> None:
    val = input(f"Filter readiness {READINESS}: ").strip().lower()
    if not val:
        print("No filter provided.")
        return
    if hasattr(_LIB, "filter_by_readiness"):
        _LIB.filter_by_readiness(val)
    else:
        found = False
        for p in _LIB.pieces:
            if (getattr(p, "readiness_status", "") or "").strip().lower() == val:
                print("-", _fmt_piece(p))
                found = True
        if not found:
            print(f"No pieces found with '{val}'.")
