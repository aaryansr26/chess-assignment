from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)

def get_position(position):
    row, col = ord(position[1]) - ord('1'), ord(position[0]) - ord('A')
    return [row, col]

def get_chess_notation(row, col):
    position = chr(col + ord('A')) + chr(row + ord('1'))
    return position
    
def get_valid_moves(board, piece):
    k_moves, r_moves, q_moves, b_moves = [], [], [], []
    rook_pos, knight_pos, queen_pos, b_pos = get_position(board["Rook"]), get_position(board["Knight"]), get_position(board["Queen"]), get_position(board["Bishop"])
    
    #knight moves
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        new_row, new_col = knight_pos[0] + dr, knight_pos[1] + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            k_moves.append(get_chess_notation(new_row, new_col))
    
    #rook moves
    for dr in range(-8, 8):
        new_row, new_col = rook_pos[0] + dr, rook_pos[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if[new_row, new_col] != [rook_pos[0], rook_pos[1]]:
                r_moves.append(get_chess_notation(new_row, new_col))
    for dc in range(-8, 8):
        new_row, new_col = rook_pos[0], rook_pos[1] + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if[new_row, new_col] != [rook_pos[0], rook_pos[1]]:
                r_moves.append(get_chess_notation(new_row, new_col))
                
    #bishop moves
    bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)] #diagonal directions
    for direction in bishop_moves:
        for i in range(1, 8):
            new_row = b_pos[0] + direction[0] * i
            new_col = b_pos[1] + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8: #ensure within bounds
                if[new_row, new_col] != [b_pos[0], b_pos[1]]:
                    b_moves.append(get_chess_notation(new_row, new_col))
                    
    #queen moves
    queen_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
    for direction in queen_moves:
        for i in range(1, 8):
            new_row = queen_pos[0] + direction[0] * i
            new_col = queen_pos[1] + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if [new_row, new_col] != [queen_pos[0], queen_pos[1]]:
                    q_moves.append(get_chess_notation(new_row, new_col))
                    
    if piece == "knight":
        all_threats = set(b_moves) | set(q_moves) | set(r_moves)
        safe_moves = set(k_moves) - all_threats
        
    elif piece == "queen":
        all_threats = set(b_moves) | set(k_moves) | set(r_moves)
        safe_moves = set(q_moves) - all_threats
        
    elif piece == "rook":
        all_threats = set(b_moves) | set(q_moves) | set(k_moves)
        safe_moves = set(r_moves) - all_threats
    else:
        all_threats = set(r_moves) | set(q_moves) | set(k_moves)
        safe_moves = set(b_moves) - all_threats
        
    return list(safe_moves) 
    

@app.get("/chess/<piece>")
def chess_moves(piece):
    data = request.json
    board = data["positions"]
    valid_positions = []
     
    valid_positions = sorted(get_valid_moves(board, piece))
    
    
    
    return jsonify({"valid_moves" : valid_positions})

    
if __name__=="__main__":
    app.run(debug=True)