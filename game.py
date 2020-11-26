import random
import time


def add_new_tile(board, open_tiles):
    """Adds new tiles to the playing board"""
    num = random.choice([2, 4])
    if open_tiles:
        new_key = random.choice(open_tiles)
        board.create_tile(new_key)
        board.change_tile_appearance(new_key, num)
    else:
        print('Game Over')
        board.end_game()


def try_merging(board, curr_key, new_key, merge_ls):
    """Tries to merge tiles at curr_key and new_key"""
    if board.tiles[new_key] and can_merge(board, curr_key, new_key) and (new_key not in merge_ls):
        return board.merge(curr_key, new_key, merge_ls)
    else:
        return False


def can_merge(board, curr_key, new_key):
    """Checks if there are filled tiles in between and determines whether
    a merge is then possible"""
    if curr_key[0] == new_key[0]:
        if abs(curr_key[1] - new_key[1]) == 1:
            return True
        start = min(curr_key, new_key)
        end = max(curr_key, new_key)
        in_between = [(curr_key[0], i) for i in range(start[1] + 1, end[1])]
        if list(filter(lambda key: key in board.filled, in_between)) == []:
            return True
        else:
            return False
    elif curr_key[1] == new_key[1]:
        if abs(curr_key[0] - new_key[0]) == 1:
            return True
        start = min(curr_key, new_key)
        end = max(curr_key, new_key)
        in_between = [(i, curr_key[1]) for i in range(start[0] + 1, end[0])]
        if list(filter(lambda key: key in board.filled, in_between)) == []:
            return True
        else:
            return False
    else:
        return False


def move_tile(board, search, lock, sort_f, next_best_f):
    """Moves a tile to a new location based on a search function"""
    tiles = board.tiles
    filled_keys = sort_f(board.filled)

    def moving_to(curr_key, new):
        """Checks conditions of each move"""
        if new == curr_key:
            return False
        if new not in board.filled:
            board.create_tile(new)
            board.change_tile_appearance(new, curr_key, update=True)
            board.remove_tile(curr_key)
            return True
        else:
            merge_result = try_merging(board, curr_key, new, results_of_merges)
            if not merge_result:
                next_key = next_best_f(new)
                if next_key in tiles:
                    return moving_to(curr_key, next_key)

    # list that holds keys that are results of merges during every move
    results_of_merges = []
    for key in filled_keys[:]:
        # returns the key with farthest movement (ideal spot)
        new_key = search(lock(tiles.keys(), key))
        moving_to(key, new_key)

    open_tiles_keys = list(
        filter(lambda key: key not in board.filled, tiles.keys()))
    add_new_tile(board, open_tiles_keys)


def create_dir(direction, board):
    """Returns a function that moves a tile according to direction"""
    def dir_func(e):
        def row_lock(it, k): return list(filter(lambda x: x[0] == k[0], it))
        def col_lock(it, k): return list(filter(lambda x: x[1] == k[1], it))

        if direction == 'L':
            def l_search(it): return min(it, key=lambda x: x[1])
            def sort_l(it): return sorted(it, key=lambda x: x[1])
            def next_l(key): return (key[0], key[1] + 1)
            move_tile(board, l_search, row_lock, sort_l, next_l)

        elif direction == 'R':
            def r_search(it): return max(it, key=lambda x: x[1])
            def sort_r(it): return sorted(it, key=lambda x: -x[1])
            def next_r(key): return (key[0], key[1] - 1)
            move_tile(board, r_search, row_lock, sort_r, next_r)

        elif direction == 'U':
            def u_search(it): return min(it, key=lambda x: x[0])
            def sort_u(it): return sorted(it, key=lambda x: x[0])
            def next_u(key): return (key[0] + 1, key[1])
            move_tile(board, u_search, col_lock, sort_u, next_u)

        elif direction == 'D':
            def d_search(it): return max(it, key=lambda x: x[0])
            def sort_d(it): return sorted(it, key=lambda x: -x[0])
            def next_d(key): return (key[0] - 1, key[1])
            move_tile(board, d_search, col_lock, sort_d, next_d)

    return dir_func
