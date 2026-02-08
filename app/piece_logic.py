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
    

    def delete_piece(self, piece_id):
        for piece in self.pieces:
            if piece.piece_id == piece_id:
                self.pieces.remove(piece)
                return True
        return False



    # Displays all the pieces in no particular order
    def list_pieces(self):
        for piece in self.pieces:
            if piece.updated:
                print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}, {piece.updated}')
            else:
                print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}')


    def filter_by_readiness(self, readiness_status):
        found = False

        for piece in self.pieces:
            if piece.readiness_status.lower() == readiness_status.lower():
                found = True
                if piece.updated:
                    print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}, {piece.updated}')
                else:
                    print(f'{piece.piece_id} - {piece.title}: {piece.composer}, {piece.genre}, {piece.readiness_status}, {piece.created}')

        
        if not found:
            print(f'No pieces found with {readiness_status} readiness status.')






if __name__ == '__main__':
    library = PieceLibrary()

    p1 = Piece(1, "The Ruins of Athens", "Beethoven", "Classical", "Ready", 12)
    p2 = Piece(2, "Pet Sounds", "The Beach Boys", "Chamber Pop", "Learning", 14)
    p3 = Piece(3, "XX", "The xx", "Classical", "Indie Pop", 16)
    p4 = Piece(4, "Jaws", "John Williams", "Classical", "Ready", 22)

    # Testing add_piece
    library.add_piece(p1)
    library.add_piece(p2)
    library.add_piece(p3)
    library.add_piece(p4)
    #Testing list_pieces
    print(f'List Pieces:\n')
    library.list_pieces()


    #Testing edit_piece
    library.edit_piece(2, "The Lonly Shepherd", "Zamfir", "Classical", "Rehearsing")
    print(f'\nEdited Pieces:\n')
    library.list_pieces() 


    # Testing delete_piece
    library.delete_piece(3)
    print(f'\nDeleted Pieces:\n')
    library.list_pieces()


    #Testing filter_by_readiness
    print(f'\nFilter:\n')
    library.filter_by_readiness("Ready")
