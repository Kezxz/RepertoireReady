from piece_bridge import (
    load_from_csv, save_to_csv,
    list_pieces, add_piece, edit_piece, delete_piece, filter_by_readiness, filter_by_attribute,
    exists_piece_id,
)
from setlist_bridge import (
    load_setlists, save_setlists,
    list_setlists, add_setlist, view_setlist,
    add_piece_to_setlist, remove_piece_from_setlist, delete_setlist
)

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
        elif choice == "6"; filter_by_attribute()
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
        elif choice == "3": view_setlist(exists_piece_id)
        elif choice == "4": add_piece_to_setlist(exists_piece_id)
        elif choice == "5": remove_piece_from_setlist()
        elif choice == "6": delete_setlist()
        elif choice == "7": return
        else: print("Invalid.")

def main():
    load_from_csv()
    load_setlists()
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
                save_to_csv(); save_setlists(); print("Saved.")
            elif choice == "4":
                save_to_csv(); save_setlists(); print("Saved. Goodbye!"); break
            else: print("Invalid.")
    except KeyboardInterrupt:
        print("\nInterrupted. Saving...")
        save_to_csv(); save_setlists(); print("Saved. Goodbye!")

if __name__ == "__main__":
    main()
