test = {(6, 5): [(5, 4)], (4, 5): [(3, 6), (2, 3)], (5, 0): [(4, 1)], (5, 6): [(4, 7)], (6, 3): [(5, 4)], (5, 2): [(4, 3), (4, 1)]}

jump_moves = {}
for piece, moves in test.items():
    for move in moves:
        if abs(move[0] - piece[0]) != 1:
            jump_moves[piece] = jump_moves.get(piece, []) + [move]
print(jump_moves)