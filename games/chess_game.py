"""
Chess Engine with Interactive Board and Heuristic AI for GitHub Profile Arcade.
Generates live SVG chessboard (assets/chess_board.svg) and cleanly formatted move tables.
"""

import json
import os
import random
from typing import Dict, Any, Tuple, Optional
import chess
import chess.svg

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "chess.json")
SVG_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "chess_board.svg")
REPO_OWNER = "sudo-aadarsh"
REPO_NAME = "sudo-aadarsh"

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}


def issue_url(title: str, body: str) -> str:
    from urllib.parse import quote_plus
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?title={quote_plus(title)}&body={quote_plus(body)}"


def default_state() -> Dict[str, Any]:
    b = chess.Board()
    return {
        "fen": b.fen(),
        "status": "in_progress",
        "last_player": None,
        "winner": None,
        "last_move_uci": None,
        "last_move_san": None,
        "move_history": []
    }


def load_state() -> Dict[str, Any]:
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_state()


def save_state(state: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def render_svg(board: chess.Board, last_move: Optional[chess.Move] = None) -> None:
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    check_sq = board.king(board.turn) if board.is_check() else None
    svg_data = chess.svg.board(
        board=board,
        size=420,
        lastmove=last_move,
        check=check_sq,
        colors={
            "square light": "#eaebd0",
            "square dark": "#779954",
            "margin": "#161b22",
            "coord": "#8b949e"
        }
    )
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_data)


def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return 99999 if board.turn == chess.WHITE else -99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES.get(piece.piece_type, 0)
            score += -val if piece.color == chess.WHITE else val
    return score


def choose_ai_move(board: chess.Board) -> Optional[chess.Move]:
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    best_score = -999999
    best_moves = []

    for move in legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return move

        reply_score = 999999
        replies = list(board.legal_moves)
        if not replies:
            score = 0
        else:
            for rep in replies:
                board.push(rep)
                val = evaluate_board(board)
                board.pop()
                if val < reply_score:
                    reply_score = val
            score = reply_score

        board.pop()

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves) if best_moves else random.choice(legal_moves)


def process_move(move_str: str, username: str) -> Tuple[bool, str, int, bool, bool]:
    state = load_state()
    board = chess.Board(state["fen"])

    if state["status"] != "in_progress" or board.is_game_over():
        return False, "This chess game has ended! Click [Start New Chess Game] to play again.", 0, False, False

    clean_str = move_str.strip()
    parsed_move = None

    try:
        parsed_move = chess.Move.from_uci(clean_str.lower())
        if parsed_move not in board.legal_moves:
            parsed_move = None
    except Exception:
        pass

    if not parsed_move:
        try:
            parsed_move = board.parse_san(clean_str)
        except Exception:
            pass

    if not parsed_move or parsed_move not in board.legal_moves:
        legal_san = [board.san(m) for m in list(board.legal_moves)[:8]]
        return False, f"Illegal chess move: `{move_str}`. Legal moves include: {', '.join(legal_san)}...", 0, False, False

    san_player = board.san(parsed_move)
    board.push(parsed_move)
    state["last_player"] = username
    state["last_move_uci"] = parsed_move.uci()
    state["last_move_san"] = san_player
    history = state.setdefault("move_history", [])
    history.append(f"@{username}: {san_player}")

    if board.is_checkmate():
        state["status"] = "won_player"
        state["winner"] = username
        state["fen"] = board.fen()
        save_state(state)
        render_svg(board, parsed_move)
        return True, f"👑 CHECKMATE! @{username} defeated Aadarsh-AI with `{san_player}`! (+50 pts)", 50, True, False

    if board.is_game_over():
        state["status"] = "draw"
        state["fen"] = board.fen()
        save_state(state)
        render_svg(board, parsed_move)
        return True, f"🤝 Game ended in a DRAW with `{san_player}`!", 15, False, True

    # AI Turn
    ai_move = choose_ai_move(board)
    ai_san = board.san(ai_move)
    board.push(ai_move)
    history.append(f"Aadarsh-AI: {ai_san}")
    state["last_move_uci"] = ai_move.uci()
    state["last_move_san"] = ai_san

    if board.is_checkmate():
        state["status"] = "won_ai"
        state["winner"] = "Aadarsh-AI"
        state["fen"] = board.fen()
        save_state(state)
        render_svg(board, ai_move)
        return True, f"🤖 Checkmate! Aadarsh-AI won with `{ai_san}`. Well played @{username}!", 2, False, False

    if board.is_game_over():
        state["status"] = "draw"
        state["fen"] = board.fen()
        save_state(state)
        render_svg(board, ai_move)
        return True, f"🤝 Game ended in a DRAW after `{ai_san}`!", 15, False, True

    state["fen"] = board.fen()
    save_state(state)
    render_svg(board, ai_move)
    return True, f"Move `{san_player}` accepted! Aadarsh-AI countered with `{ai_san}`.", 2, False, False


def reset_game() -> str:
    state = default_state()
    save_state(state)
    b = chess.Board()
    render_svg(b)
    return "Chess match has been reset to starting position!"


def render_markdown() -> str:
    state = load_state()
    board = chess.Board(state["fen"])
    status = state["status"]
    history = state.get("move_history", [])

    last_m = None
    if state.get("last_move_uci"):
        try:
            last_m = chess.Move.from_uci(state["last_move_uci"])
        except Exception:
            pass
    render_svg(board, last_m)

    md = []
    md.append("### ♟️ Game 3: Community Chess vs Aadarsh-AI")
    md.append("> **Goal:** Outsmart Aadarsh-AI! You play White ⚪, Aadarsh-AI plays Black ⚫. Click any move below to play!\n")

    md.append('<div align="center">\n')
    md.append('  <img src="assets/chess_board.svg" alt="Live Chess Board" width="400"/>\n')

    if status == "in_progress":
        if board.is_check():
            md.append("\n> ⚠️ **CHECK! White King is under attack!**\n")

        # Build clean 4-column legal moves table
        legal_moves = list(board.legal_moves)
        top_moves = legal_moves[:8]

        move_links = []
        for m in top_moves:
            san = board.san(m)
            url = issue_url(
                f"arcade:chess:move:{m.uci()}",
                f"Click 'Submit new issue' to play `{san}` ({m.uci()})!\n\n*(Automated chess move)*"
            )
            move_links.append(f"[ `{san}` ]({url})")

        md.append("**⚡ Quick Suggested Moves for White:**\n")
        md.append("| Move Option 1 | Move Option 2 | Move Option 3 | Move Option 4 |")
        md.append("| :---: | :---: | :---: | :---: |")

        row1 = move_links[0:4]
        row2 = move_links[4:8]
        if row1:
            while len(row1) < 4:
                row1.append("-")
            md.append("| " + " | ".join(row1) + " |")
        if row2:
            while len(row2) < 4:
                row2.append("-")
            md.append("| " + " | ".join(row2) + " |")

        custom_url = issue_url(
            "arcade:chess:move:e4",
            "Replace 'e4' in the title above with your desired SAN move (e.g. Nf3, Bb5, O-O, d4) and submit this issue!"
        )
        reset_url = issue_url(
            "arcade:chess:new",
            "Click 'Submit new issue' to reset the chessboard to start a new game!"
        )

        md.append(f"\n[ ✍️ Submit Any Custom Move ]({custom_url}) &nbsp;|&nbsp; [ 🔄 Start New Chess Match ]({reset_url})\n")

    elif status == "won_player":
        winner = state.get("winner", "Visitor")
        md.append(f"🏆 **CHECKMATE!** [@{winner}](https://github.com/{winner}) defeated Aadarsh-AI! (+50 pts 👑)\n")
    elif status == "won_ai":
        md.append("🤖 **Checkmate!** Aadarsh-AI won this match!\n")
    else:
        md.append("🤝 **Game Over:** Draw / Stalemate!\n")

    md.append("</div>\n")

    hist_str = " &nbsp;|&nbsp; ".join(history[-4:]) if history else "Game just began (1. e4...)"
    md.append(f"**Last Plays:** `{hist_str}`\n")

    return "\n".join(md)
