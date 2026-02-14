import piece_logic as tpl
from storage import load_pieces, save_pieces, load_setlists, save_setlists

from services import (
    # pieces
    list_pieces, add_piece, edit_piece, delete_piece, filter_by_readiness, filter_by_attribute, piece_exists,
    # setlists
    list_setlists, add_setlist, view_setlist, add_piece_to_setlist, remove_piece_from_setlist, delete_setlist,
)

# in-memory state
LIB = tpl.PieceLibrary()
performances = {}
setlist_items = []

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
        if choice == "1": list_pieces(LIB)
        elif choice == "2": add_piece(LIB)
        elif choice == "3": edit_piece(LIB)
        elif choice == "4": delete_piece(LIB)
        elif choice == "5": filter_by_readiness(LIB)
        elif choice == "6": filter_by_attribute(LIB)
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
        if choice == "1": list_setlists(performances, setlist_items)
        elif choice == "2": add_setlist(performances)
        elif choice == "3": view_setlist(performances, setlist_items)
        elif choice == "4": add_piece_to_setlist(performances, setlist_items, lambda pid: piece_exists(LIB, pid))
        elif choice == "5": remove_piece_from_setlist(setlist_items)
        elif choice == "6": delete_setlist(performances, setlist_items)
        elif choice == "7": return
        else: print("Invalid.")

# ----------- App ----------- #

def main():
    LIB.pieces = load_pieces()    # load persistence
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
