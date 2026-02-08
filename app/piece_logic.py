# piece related logic

# add_piece()
# list_pieces()
# edit_piece()
# delete_piece()
# filter_by_readiness()





from datetime import date

# Piece class (Parent class)
class Piece:
    def __init__(self, piece_id, title, composer, genre, readiness_status, user_id):
        self.piece_id = piece_id
        self.title = title
        self.composer = composer
        self.genre = genre
        self.readiness_status = readiness_status
        self.user_id = user_id

        self.created = None
        self.updated = None


# Creates an array of pieces
class PieceLibrary():
    def __init__(self):
        self.pieces = []

    # adds new pieces to the array and adds the date the were created
    def add_piece(self, piece):
        piece.created = date.today()
        self.pieces.append(piece)


    def edit_piece(self, piece_id, new_title, new_composer, new_genre, new_readiness_status):
        for piece in self.pieces:
            if piece.piece_id == piece_id:
                piece.title = new_title
                piece.composer = new_composer
                piece.genre = new_genre
                piece.readiness_status = new_readiness_status

                piece.updated = date.today()
                return True
            
        return False



    # Displays all the pieces in no particular order
    def list_pieces(self):
        for piece in self.pieces:
            if piece.updated:
                print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}, {piece.updated}')
            else:
                print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}')




if __name__ == '__main__':
    library = PieceLibrary()

    p1 = Piece(1, "The Ruins of Athens", "Beethoven", "Classical", "Ready", 12)
    p2 = Piece(2, "Happy", "John", "Pop", "Prep", 14)

    library.add_piece(p1)
    library.add_piece(p2)

    library.list_pieces()

    library.edit_piece(2, "Sad", "Alex", "Metal", "Not Ready")

    library.list_pieces() 