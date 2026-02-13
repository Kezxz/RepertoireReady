import piece_logic as tpl
import setlist_logic as sl
from storage import load_pieces, save_pieces, load_setlists, save_setlists

READINESS = ["learning", "rehearsing", "performance-ready"]

# in-memory state
LIB = tpl.PieceLibrary()
performances = {}
setlist_items = []

# ----------- Basic Helpers ----------- #

def next_piece_id() -> int:
    return max([p.piece_id for p in LIB.pieces], default = 0) + 1

def piece_exists(pid: int) -> bool:
    return any(p.piece_id == pid for p in LIB.pieces)

def next_setlist_id() -> int:
    return max(performances.keys(), default = 0) +1

# ----------- Pieces UI ----------- #

def fmt_piece(p: tpl.Piece) -> str:
    return f"#{p.piece_id} {p.title} — {p.composer} [{p.genre}] readiness={p.readiness_status}"

def list_pieces():
    if not LIB.pieces:
        print("No pieces yet."); return
    for p in LIB.pieces:
        print("-", fmt_piece(p))

def add_piece():
    title = input("Title: ").strip()
    if not title:
        print("Title is required."); return
    composer = input("Composer: ").strip()
    genre = input("Genre/Key: ").strip()
    print(f"Readiness options: {READINESS}")
    r = (input("Readiness [learning]: ").strip().lower() or "learning")
    if r not in READINESS:
        r = "learning"

    p = tpl.Piece(next_piece_id(), title, composer, genre, r, user_id=0)
    LIB.add_piece(p)   # sets created date in teammate lib
    print("Added.")

def edit_piece():
    try:
        pid = int(input("Piece id to edit: ").strip())
    except ValueError:
        print("Invalid id."); return
    cur = next((x for x in LIB.pieces if x.piece_id == pid), None)
    if not cur:
        print("Not found."); return

    title = input(f"Title [{cur.title}]: ").strip() or cur.title
    composer = input(f"Composer [{cur.composer}]: ").strip() or cur.composer
    genre = input(f"Genre/Key [{cur.genre}]: ").strip() or cur.genre
    r = input(f"Readiness {READINESS} [{cur.readiness_status}]: ").strip().lower() or cur.readiness_status
    if r not in READINESS:
        r = cur.readiness_status

    LIB.edit_piece(pid, title, composer, genre, r)
    print("Updated.")

def delete_piece():
    try:
        pid = int(input("Piece id to delete: ").strip())
    except ValueError:
        print("Invalid id."); return
    ok = LIB.delete_piece(pid)
    print("Deleted." if ok else "Not found.")

def filter_by_readiness():
    print(f"\nReadiness options: {READINESS}")
    val = input("Show pieces with status: ").strip().lower()
    if not val:
        print("No status entered."); return
    if val not in READINESS:
        print(f"Unknown status '{val}'."); return
    matches = [p for p in LIB.pieces if (getattr(p, "readiness_status","") or "").lower() == val]
    if not matches:
        print(f"No pieces found with readiness '{val}'.")
    else:
        print(f"\n--- Results for: {val} ---")
        for p in matches:
            print("-", fmt_piece(p))

def filter_by_attribute():
    print("\nSearch by: 1) Composer 2) Genre")
    choice = input("> ").strip()
    attr = "composer" if choice == "1" else "genre" if choice == "2" else None
    if not attr:
        print("Invalid option."); return
    q = input(f"Enter {attr}: ").strip().lower()
    matches = [p for p in LIB.pieces if q in (getattr(p, attr, "") or "").lower()]
    if not matches:
        print(f"No matches for {attr}: '{q}'."); return
    print(f"\n--- Results for {attr.capitalize()}: {q} ---")
    for p in matches:
        print("-", fmt_piece(p))

# ----------- Setlist UI ----------- #

def list_setlists():
    if not performances:
        print("No setlists yet."); return
    for pid, perf in performances.items():
        count = sum(1 for it in setlist_items if it.performance_id == pid)
        print(f"- #{pid} {perf.title} (pieces: {count})")

def add_setlist():
    title = input("Setlist title: ").strip()
    date  = input("Date (free text ok): ").strip()
    loc   = input("Location (optional): ").strip()
    pid = next_setlist_id()
    performances[pid] = sl.Performance(pid, title, date, loc, 0)
    print(f"Added setlist #{pid}.")

def view_setlist():
    try:
        pid = int(input("Setlist id to view: ").strip())
    except ValueError:
        print("Invalid id."); return
    perf = performances.get(pid)
    if not perf:
        print("Not found."); return
    sl.view_setlist(perf, setlist_items)

def add_piece_to_setlist():
    try:
        pid = int(input("Setlist id: ").strip())
        piece_id = int(input("Piece id to add: ").strip())
    except ValueError:
        print("Invalid id."); return
    if pid not in performances:
        print("Setlist not found."); return
    if not piece_exists(piece_id):
        print("That piece does not exist."); return
    # prevent duplicates
    if any((it.performance_id == pid and it.piece_id == piece_id) for it in setlist_items):
        print("That piece is already in this setlist."); return
    sl.add_piece_to_setlist(setlist_items, pid, piece_id)
    print("Added.")

def remove_piece_from_setlist():
    try:
        pid = int(input("Setlist id: ").strip())
        order_index = int(input("Order number to remove: ").strip())
    except ValueError:
        print("Invalid number."); return
    ok = sl.remove_piece_from_setlist(setlist_items, pid, order_index)
    print("Removed." if ok else "Not found at that order.")

def delete_setlist():
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

# ----------- Menus ----------- #

def pieces_menu():
    while True:
        print("\nPieces Menu")
        print("1) List pieces")
        print("2) Add piece")
        print("3) Edit piece")
        print("4) Delete piece")
        print("5) Filter by readiness")
        print("6) Search by Composer/Genre")
        print("7) Back")
        choice = input("> ").strip()
        if choice == "1": list_pieces()
        elif choice == "2": add_piece()
        elif choice == "3": edit_piece()
        elif choice == "4": delete_piece()
        elif choice == "5": filter_by_readiness()
        elif choice == "6": filter_by_attribute()
        elif choice == "7": return
        else: print("Invalid.")

def setlists_menu():
    while True:
        print("\nSetlists Menu")
        print("1) List setlists")
        print("2) Add setlist")
        print("3) View setlist")
        print("4) Add piece to setlist")
        print("5) Remove piece from setlist")
        print("6) Delete setlist")
        print("7) Back")
        choice = input("> ").strip()
        if choice == "1": list_setlists()
        elif choice == "2": add_setlist()
        elif choice == "3": view_setlist()
        elif choice == "4": add_piece_to_setlist()
        elif choice == "5": remove_piece_from_setlist()
        elif choice == "6": delete_setlist()
        elif choice == "7": return
        else: print("Invalid.")

# ----------- App ----------- #

def main():
    LIB.pieces = load_pieces()
    global performances, setlist_items
    performances, setlist_items = load_setlists()
    

    try:
        while True:
            print("\nRepertoireReady")
            print("1) Pieces")
            print("2) Setlists")
            print("3) Save")
            print("4) Quit")
            choice = input("> ").strip()
            if choice == "1": pieces_menu()
            elif choice == "2": setlists_menu()
            elif choice == "3":
                save_pieces(LIB.pieces); save_setlists(performances, setlist_items); print("Saved.")
            elif choice == "4":
                save_pieces(LIB.pieces); save_setlists(performances, setlist_items); print("Saved. Goodbye!"); break
            else: print("Invalid.")
    except KeyboardInterrupt:
        print("\nInterrupted. Saving...")
        save_pieces(LIB.pieces); save_setlists(performances, setlist_items); print("Saved. Goodbye!")

if __name__ == "__main__":
    main()
