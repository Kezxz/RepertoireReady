import piece_logic as tpl
import setlist_logic as sl

READINESS = ["learning", "rehearsing", "performance-ready"]

# ----------- Pieces ----------- #

def _next_piece_id(lib: tpl.PieceLibrary) -> int:
    return max([p.piece_id for p in lib.pieces], default=0) + 1

def piece_exists(lib: tpl.PieceLibrary, pid: int) -> bool:
    return any(p.piece_id == pid for p in lib.pieces)

def _fmt_piece(p: tpl.Piece) -> str:
    return f"#{p.piece_id} {p.title} — {p.composer} [{p.genre}] readiness={p.readiness_status}"

def list_pieces(lib: tpl.PieceLibrary) -> None:
    if not lib.pieces:
        print("No pieces yet."); return
    for p in lib.pieces:
        print("-", _fmt_piece(p))

def add_piece(lib: tpl.PieceLibrary) -> None:
    title = input("Title: ").strip()
    if not title:
        print("Title is required."); return
    composer = input("Composer: ").strip()
    genre = input("Genre/Key: ").strip()
    print(f"Readiness options: {READINESS}")
    r = (input("Readiness [learning]: ").strip().lower() or "learning")
    r = r.replace(" ", "-").replace("_", "-")
    if r not in READINESS:
        r = "learning"

    p = tpl.Piece(_next_piece_id(lib), title, composer, genre, r, user_id=0)
    lib.add_piece(p)
    print("Added.")

def edit_piece(lib: tpl.PieceLibrary) -> None:
    try:
        pid = int(input("Piece id to edit: ").strip())
    except ValueError:
        print("Invalid id."); return

    cur = next((x for x in lib.pieces if x.piece_id == pid), None)
    if not cur:
        print("Not found."); return

    title = input(f"Title [{cur.title}]: ").strip() or cur.title
    composer = input(f"Composer [{cur.composer}]: ").strip() or cur.composer
    genre = input(f"Genre/Key [{cur.genre}]: ").strip() or cur.genre
    r = (input(f"Readiness {READINESS} [{cur.readiness_status}]: ").strip().lower()
         or cur.readiness_status)
    r = r.replace(" ", "-").replace("_", "-")
    if r not in READINESS:
        r = cur.readiness_status

    lib.edit_piece(pid, title, composer, genre, r)
    print("Updated.")

def delete_piece(lib: tpl.PieceLibrary) -> None:
    try:
        pid = int(input("Piece id to delete: ").strip())
    except ValueError:
        print("Invalid id."); return
    ok = lib.delete_piece(pid)
    print("Deleted." if ok else "Not found.")

def filter_by_readiness(lib: tpl.PieceLibrary) -> None:
    print(f"\nReadiness options: {READINESS}")
    val = (input("Show pieces with status: ").strip().lower()
           .replace(" ", "-").replace("_", "-"))
    if not val:
        print("No status entered."); return
    if val not in READINESS:
        print(f"Unknown status '{val}'."); return

    matches = [p for p in lib.pieces if (getattr(p, "readiness_status", "") or "").lower() == val]
    if not matches:
        print(f"No pieces found with readiness '{val}'.")
    else:
        print(f"\n--- Results for: {val} ---")
        for p in matches:
            print("-", _fmt_piece(p))

def filter_by_attribute(lib: tpl.PieceLibrary) -> None:
    print("\nSearch by: 1) Composer 2) Genre")
    choice = input("> ").strip()
    attr = "composer" if choice == "1" else "genre" if choice == "2" else None
    if not attr:
        print("Invalid option."); return
    q = input(f"Enter {attr}: ").strip().lower()
    matches = [p for p in lib.pieces if q in (getattr(p, attr, "") or "").lower()]
    if not matches:
        print(f"No matches for {attr}: '{q}'."); return
    print(f"\n--- Results for {attr.capitalize()}: {q} ---")
    for p in matches:
        print("-", _fmt_piece(p))


# ----------- Setlists ----------- #

def _next_setlist_id(performances: dict[int, sl.Performance]) -> int:
    return max(performances.keys(), default=0) + 1

def list_setlists(performances: dict[int, sl.Performance], setlist_items: list[sl.Setlist_Item]) -> None:
    if not performances:
        print("No setlists yet."); return
    for pid, perf in performances.items():
        count = sum(1 for it in setlist_items if it.performance_id == pid)
        print(f"- #{pid} {perf.title} (pieces: {count})")

def add_setlist(performances: dict[int, sl.Performance]) -> None:
    title = input("Setlist title: ").strip()
    date  = input("Date (free text ok): ").strip()
    loc   = input("Location (optional): ").strip()
    pid = _next_setlist_id(performances)
    performances[pid] = sl.Performance(pid, title, date, loc, 0)
    print(f"Added setlist #{pid}.")

def view_setlist(performances: dict[int, sl.Performance], setlist_items: list[sl.Setlist_Item]) -> None:
    try:
        pid = int(input("Setlist id to view: ").strip())
    except ValueError:
        print("Invalid id."); return
    perf = performances.get(pid)
    if not perf:
        print("Not found."); return
    sl.view_setlist(perf, setlist_items)

def add_piece_to_setlist(performances: dict[int, sl.Performance],
                         setlist_items: list[sl.Setlist_Item],
                         piece_exists_fn) -> None:
    try:
        pid = int(input("Setlist id: ").strip())
        piece_id = int(input("Piece id to add: ").strip())
    except ValueError:
        print("Invalid id."); return
    if pid not in performances:
        print("Setlist not found."); return
    if not piece_exists_fn(piece_id):
        print("That piece does not exist."); return
    # prevent duplicates
    if any((it.performance_id == pid and it.piece_id == piece_id) for it in setlist_items):
        print("That piece is already in this setlist."); return
    sl.add_piece_to_setlist(setlist_items, pid, piece_id)
    print("Added.")

def remove_piece_from_setlist(setlist_items: list[sl.Setlist_Item]) -> None:
    try:
        pid = int(input("Setlist id: ").strip())
        order_index = int(input("Order number to remove: ").strip())
    except ValueError:
        print("Invalid number."); return
    ok = sl.remove_piece_from_setlist(setlist_items, pid, order_index)
    print("Removed." if ok else "Not found at that order.")

def delete_setlist(performances: dict[int, sl.Performance], setlist_items: list[sl.Setlist_Item]) -> None:
    try:
        pid = int(input("Setlist id to delete: ").strip())
    except ValueError:
        print("Invalid id."); return
    if pid not in performances:
        print("Not found."); return
    del performances[pid]
    for it in list(setlist_items):
        if it.performance_id == pid:
            setlist_items.remove(it)
    print("Deleted.")