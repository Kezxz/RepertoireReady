# setlist related logic

# create_setlist()
# add_piece_to_setlist()
# remove_piece_from_setlist()
# view_setlist()
# move_up() and move_down()

class Performance:
    def __init__(self, performance_id, title, date, location, user_id):
        self.performance_id = performance_id
        self.title = title
        self.date = date
        self.location = location
        self.user_id = user_id

    def show(self):
        print(f"Setlist: {self.title} | {self.date} | {self.location} | user={self.user_id}")

class Setlist_Item:
    def __init__(self, setlist_item_id, performance_id, piece_id, order_index):
        self.setlist_item_id = setlist_item_id
        self.performance_id = performance_id
        self.piece_id = piece_id
        self.order_index = order_index

    def show(self):
        print(f"{self.order_index}. piece_id={self.piece_id} (item_id={self.setlist_item_id})")

def create_setlist(performance_id, title, date, location, user_id):
    """
    Creates a setlist (Performance).
    """
    return Performance(performance_id, title, date, location, user_id)


def add_piece_to_setlist(setlist_items, performance_id, piece_id):
    """
    Adds a piece to the end of the setlist as a Setlist_Item.
    """
    current = [it for it in setlist_items if it.performance_id == performance_id]
    next_order = len(current) + 1
    next_item_id = len(setlist_items) + 1

    item = Setlist_Item(next_item_id, performance_id, piece_id, next_order)
    setlist_items.append(item)
    return item

def remove_piece_from_setlist(setlist_items, performance_id, order_index):
    """
    Removes a piece from the setlist by its order number (order_index).
    Then renumbers the remaining items to keep order clean.
    """
    for it in list(setlist_items):
        if it.performance_id == performance_id and it.order_index == order_index:
            setlist_items.remove(it)
            _renumber_setlist(setlist_items, performance_id)
            return True
    return False

def view_setlist(setlist, setlist_items):
    """
    Prints the setlist and its items in order.
    """
    setlist.show()
    items = [it for it in setlist_items if it.performance_id == setlist.performance_id]
    items.sort(key=lambda it: it.order_index)

    if not items:
        print("(no pieces yet)")
        return

    for it in items:
        it.show()

def move_up(setlist_items, performance_id, order_index):
    """
    Moves an item up by one spot (swap with the item above).
    """
    items = [it for it in setlist_items if it.performance_id == performance_id]
    items.sort(key=lambda it: it.order_index)

    idx = order_index - 1
    if idx <= 0 or idx >= len(items):
        return False

    items[idx].order_index, items[idx - 1].order_index = items[idx - 1].order_index, items[idx].order_index
    _renumber_setlist(setlist_items, performance_id)
    return True

def move_down(setlist_items, performance_id, order_index):
    """
    Moves an item down by one spot (swap with the item below).
    """
    items = [it for it in setlist_items if it.performance_id == performance_id]
    items.sort(key=lambda it: it.order_index)

    idx = order_index - 1
    if idx < 0 or idx >= len(items) - 1:
        return False

    items[idx].order_index, items[idx + 1].order_index = items[idx + 1].order_index, items[idx].order_index
    _renumber_setlist(setlist_items, performance_id)
    return True

def _renumber_setlist(setlist_items, performance_id):
    """
    Keeps order_index clean (1..n) for one setlist.
    """
    items = [it for it in setlist_items if it.performance_id == performance_id]
    items.sort(key=lambda it: it.order_index)

    for i, it in enumerate(items, start=1):
        it.order_index = i