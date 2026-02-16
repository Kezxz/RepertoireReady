import os
import tempfile

from app import piece_logic as tpl
from app import setlist_logic as sl
from app.storage import load_pieces, save_pieces, load_setlists, save_setlists


def test_end_to_end_smoke():
    # use an isolated temp directory so we never touch repo CSVs in data/
    with tempfile.TemporaryDirectory() as tmp:
        pieces_path = os.path.join(tmp, "piece_library.csv")
        setlists_path = os.path.join(tmp, "setlist_library.csv")

# ----------- Pieces: add -> save -> load ----------- #
        
        lib = tpl.PieceLibrary()

        # create two pieces; add_piece() should set .created
        p1 = tpl.Piece(1, "Fur Elise", "Beethoven", "Classical", "learning", 0)
        p2 = tpl.Piece(2, "Take Five", "Brubeck", "Jazz", "rehearsing", 0)
        lib.add_piece(p1)
        lib.add_piece(p2)

        # test invariants before persistence
        assert p1.created is not None and p2.created is not None
        assert len(lib.pieces) == 2

        # persist and reload via storage
        save_pieces(lib.pieces, pieces_path)
        reloaded = load_pieces(pieces_path)

        # titles and readiness should be unchanged
        assert [p.title for p in reloaded] == ["Fur Elise", "Take Five"]
        assert reloaded[0].readiness_status == "learning"
        assert reloaded[1].readiness_status == "rehearsing"

# ----------- Setlists: create -> add -> save -> load ----------- #
 
        performances, items = {}, []

        # one performance with ID = 1
        performances[1] = sl.Performance(1, "Recital", "2026-02-15", "Hall", 0)

        # add the two pieces by their respective IDs
        sl.add_piece_to_setlist(items, 1, 1)
        sl.add_piece_to_setlist(items, 1, 2)

        # persist and reload setlists
        save_setlists(performances, items, setlists_path)
        perf2, items2 = load_setlists(setlists_path)

        # performance ID should exist after reload
        assert 1 in perf2

        # order is preserved
        ordered = [it.piece_id for it in sorted(items2, key=lambda x: x.order_index)]
        assert ordered == [1, 2]

# ----------- Empty setlist message ----------- #

        # add a second performance with no items
        performances[2] = sl.Performance(2, "Empty", "2026-03-01", "Grand Ole Opry", 0)

        import io, sys
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            sl.view_setlist(performances[2], items2)  # no items for performance 2
        finally:
            sys.stdout = old
        assert "(no pieces yet)" in buf.getvalue()