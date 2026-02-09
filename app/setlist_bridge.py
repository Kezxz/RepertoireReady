import csv
import os
from typing import Dict, List
import setlist_logic as sl

SETLISTS_CSV = "setlists.csv"
SETLIST_HEADER = ["id", "simple_id", "title", "date", "location", "user_id", "piece_ids"]

# in-memory state owned for bridge
_performances: Dict[int, sl.Performance] = {}
_items: List[sl.Setlist_Item] = []


# ----------- Helpers ----------- #

def _next_perf_id() -> int:
    return max(_performances.keys(), default=0) + 1

def _next_simple_setlist_id() -> int:
    used = {getattr(perf, "simple_id", 0) for perf in _performances.values() if getattr(perf, "simple_id", 0)}
    i = 1
    while i in used:
        i += 1
    return i

def _items_for(pid: int) -> List[sl.Setlist_Item]:
    return sorted([it for it in _items if it.performance_id == pid], key=lambda t: t.order_index)

# accepts: simple id, internal id, or partial title
# returns the internal setlist id
def _resolve_setlist_ref(ref: str) -> int | None:
    s = (ref or "").strip()
    if not s:
        print("No reference provided.")
        return None

    if s.isdigit():
        num = int(s)
        # check for simple_id match
        by_simple = next((pid for pid, perf in _performances.items()
                          if getattr(perf, "simple_id", None) == num), None)
        if by_simple is not None:
            return by_simple
        # if no match, check for internal id
        if num in _performances:
            return num

    # partial title match
    matches = [pid for pid, perf in _performances.items() if s.lower() in (perf.title or "").lower()]
    if not matches:
        print("No setlist matched that reference.")
        return None
    if len(matches) == 1:
        return matches[0]

    print("Multiple matches:")
    for pid in matches:
        perf = _performances[pid]
        si = getattr(perf, "simple_id", "?")
        print(f"- {si}: {perf.title}")
    pick = input("Choose simple id: ").strip()
    if pick.isdigit():
        return _resolve_setlist_ref(pick)
    return None


# ----------- Persistence (working on now) ----------- #

def load_setlists(path: str = SETLISTS_CSV) -> None:
    """Load performances + their items from CSV into in-memory state."""
    _performances.clear()
    _items.clear()

    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(SETLIST_HEADER)
        return

    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        for r in rd:
            try:
                pid = int(r.get("id") or 0)
            except ValueError:
                continue

            perf = sl.Performance(
                pid,
                r.get("title", ""),
                r.get("date", ""),
                r.get("location", ""),
                int(r.get("user_id") or 0),
            )

            si_raw = r.get("simple_id")
            perf.simple_id = int(si_raw) if (si_raw and si_raw.isdigit()) else 0

            _performances[pid] = perf

            ids = [int(x) for x in (r.get("piece_ids", "").split(";")) if x.strip()]
            for idx, piece_id in enumerate(ids, start=1):
                _items.append(sl.Setlist_Item(len(_items) + 1, pid, piece_id, idx))

    # backfill simple_id if missing
    for perf in _performances.values():
        if not getattr(perf, "simple_id", 0):
            perf.simple_id = _next_simple_setlist_id()

# save performances and their piece orders to CSV
def save_setlists(path: str = SETLISTS_CSV) -> None:
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(SETLIST_HEADER)
        for pid, perf in _performances.items():
            piece_ids = [str(it.piece_id) for it in _items_for(pid)]
            wr.writerow([pid,
                         getattr(perf, "simple_id", 0),
                         perf.title, perf.date, perf.location, perf.user_id,
                         ";".join(piece_ids)])


# ----------- CLI-facing functions ----------- #

def list_setlists() -> None:
    if not _performances:
        print("No setlists yet.")
        return
    for pid, perf in _performances.items():
        count = len(_items_for(pid))
        si = getattr(perf, "simple_id", "?")
        print(f"- #{si} {perf.title} (pieces: {count})")

def add_setlist() -> None:
    title = input("Setlist title: ").strip()
    date = input("Date (free text ok): ").strip()
    location = input("Location (optional): ").strip()
    user_id = 0
    pid = _next_perf_id()
    perf = sl.Performance(pid, title, date, location, user_id)
    perf.simple_id = _next_simple_setlist_id()
    _performances[pid] = perf
    print(f"Added setlist #{perf.simple_id}.")

def delete_setlist() -> None:
    ref = input("Setlist to delete (simple id, internal id, or partial name): ").strip()
    pid = _resolve_setlist_ref(ref)
    if pid is None:
        return
    if pid not in _performances:
        print("Not found.")
        return
    del _performances[pid]
    # remove items for this setlist
    for it in list(_items):
        if it.performance_id == pid:
            _items.remove(it)
    print("Deleted.")

def view_setlist(exists_piece_fn) -> None:
    ref = input("Setlist (simple id, internal id, or partial name): ").strip()
    pid = _resolve_setlist_ref(ref)
    if pid is None:
        return
    perf = _performances.get(pid)
    if not perf:
        print("Not found.")
        return
    sl.view_setlist(perf, _items)

def add_piece_to_setlist(exists_piece_fn) -> None:
    sref = input("Setlist (simple id, internal id, or partial name): ").strip()
    pref = input("Piece (simple id, internal id, or partial title): ").strip()
    pid = _resolve_setlist_ref(sref)
    if pid is None:
        return

    # resolve piece via piece_bridge's helper
    try:
        from piece_bridge import _resolve_piece_ref
    except Exception:
        print("Internal error resolving piece.")
        return

    internal_piece_id = _resolve_piece_ref(pref)
    if internal_piece_id is None:
        return
    if not exists_piece_fn(internal_piece_id):
        print("That piece does not exist.")
        return

    # prevent duplicates
    if any((it.performance_id == pid and it.piece_id == internal_piece_id) for it in _items):
        print("That piece is already in this setlist.")
        return

    sl.add_piece_to_setlist(_items, pid, internal_piece_id)
    print("Added.")

def remove_piece_from_setlist() -> None:
    sref = input("Setlist (simple id, internal id, or partial name): ").strip()
    pid = _resolve_setlist_ref(sref)
    if pid is None:
        return
    try:
        order_index = int(input("Order number to remove: ").strip())
    except ValueError:
        print("Invalid number.")
        return
    ok = sl.remove_piece_from_setlist(_items, pid, order_index)
    print("Removed." if ok else "Not found at that order.")