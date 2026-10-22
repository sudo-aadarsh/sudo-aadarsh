"""
Tic-Tac-Toe Engine with Tactical Minimax AI for GitHub Profile Arcade.
Grid: 3x3.
Player: ❌ (Visitor) | AI: ⭕ (Aadarsh-AI) | Empty: ⬜
"""

import json
import os
import random
from typing import Dict, Any, Tuple, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tictactoe.json")
REPO_OWNER = "sudo-aadarsh"
REPO_NAME = "sudo-aadarsh"


def issue_url(title: str, body: str) -> str:
    from urllib.parse import quote_plus
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?title={quote_plus(title)}&body={quote_plus(body)}"


def default_state() -> Dict[str, Any]:
    return {
        "board": [[" " for _ in range(3)] for _ in range(3)],
        "status": "in_progress",  # "in_progress", "won_player", "won_ai", "draw"
        "last_player": None,
        "winner": None,
        "last_move": "Waiting for challenger's first move!"
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


def check_winner(board: list) -> Optional[str]:
    # Rows & Cols
    for i in range(3):
        if board[i][0] != " " and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != " " and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Diagonals
    if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def is_full(board: list) -> bool:
    return all(cell != " " for row in board for cell in row)


def minimax(board: list, depth: int, is_maximizing: bool) -> int:
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -999
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False)
                    board[r][c] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 999
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True)
                    board[r][c] = " "
                    best_score = min(score, best_score)
        return best_score


def choose_ai_move(board: list) -> Optional[Tuple[int, int]]:
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if not empty_cells:
        return None

    # Occasionally (20% chance on first couple turns) make a tactical move to give human players a fair shot at winning!
    if len(empty_cells) >= 7 and random.random() < 0.25:
        return random.choice(empty_cells)

    best_score = -999
    best_move = None
    for (r, c) in empty_cells:
        board[r][c] = "O"
        score = minimax(board, 0, False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            best_move = (r, c)

    return best_move or random.choice(empty_cells)


def process_move(row: int, col: int, username: str) -> Tuple[bool, str, int, bool, bool]:
    """
    Processes a move at (row, col) 0-indexed.
    Returns (success, message, points_earned, won, draw).
    """
    state = load_state()

    if state["status"] != "in_progress":
        return False, "This game has finished. Click [Start New Game] to play again!", 0, False, False

    if not (0 <= row <= 2 and 0 <= col <= 2):
        return False, f"Invalid coordinates ({row}, {col}). Must be between 0 and 2.", 0, False, False

    board = state["board"]
    if board[row][col] != " ":
        return False, f"Position ({row + 1}, {col + 1}) is already taken! Choose an empty square.", 0, False, False

    # Player 1 move
    board[row][col] = "X"
    state["last_player"] = username
    state["last_move"] = f"@{username} placed ❌ at Row {row + 1}, Col {col + 1}"

    # Check player win
    if check_winner(board) == "X":
        state["status"] = "won_player"
        state["winner"] = username
        save_state(state)
        return True, f"🎉 TIC-TAC-TOE! @{username} defeated Aadarsh-AI! (+20 pts)", 20, True, False

    if is_full(board):
        state["status"] = "draw"
        save_state(state)
        return True, "🤝 Tic-Tac-Toe ended in a hard-fought DRAW!", 5, False, True

    # AI move
    ai_move = choose_ai_move(board)
    if ai_move:
        ar, ac = ai_move
        board[ar][ac] = "O"
        state["last_move"] += f" | Aadarsh-AI countered ⭕ at Row {ar + 1}, Col {ac + 1}"

        if check_winner(board) == "O":
            state["status"] = "won_ai"
            state["winner"] = "Aadarsh-AI"
            save_state(state)
            return True, f"🤖 Aadarsh-AI won this match! Try another strategy next round!", 1, False, False

        if is_full(board):
            state["status"] = "draw"
            save_state(state)
            return True, "🤝 Tic-Tac-Toe ended in a hard-fought DRAW!", 5, False, True

    save_state(state)
    return True, f"Move accepted! Aadarsh-AI responded at Row {ar + 1}, Col {ac + 1}.", 1, False, False


def reset_game() -> str:
    state = default_state()
    save_state(state)
    return "Tic-Tac-Toe has been reset! Ready for a new challenger."


def render_markdown() -> str:
    state = load_state()
    board = state["board"]
    status = state["status"]
    last_move = state.get("last_move", "No moves yet.")

    md = []
    md.append("### ❌ Game 2: Tic-Tac-Toe vs Aadarsh-AI")
    md.append("> **Rules:** Play ❌ against Aadarsh-AI's ⭕. Click any empty square `[ ⬜ ]` to place your mark!\n")

    md.append("| Col 1 | Col 2 | Col 3 |")
    md.append("| :---: | :---: | :---: |")

    for r in range(3):
        row_cells = []
        for c in range(3):
            cell = board[r][c]
            if cell == "X":
                row_cells.append("❌")
            elif cell == "O":
                row_cells.append("⭕")
            else:
                if status == "in_progress":
                    url = issue_url(
                        f"arcade:ttt:move:{r},{c}",
                        f"Click 'Submit new issue' to play ❌ at Row {r + 1}, Column {c + 1}!\n\n*(Automated move)*"
                    )
                    row_cells.append(f"[ ⬜ ]({url})")
                else:
                    row_cells.append("⬜")
        md.append(f"| {' | '.join(row_cells)} |")

    md.append("")
    if status == "in_progress":
        md.append("**Status:** ❌ **Visitor's Turn** vs ⭕ **Aadarsh-AI** &nbsp;|&nbsp; *Click any empty square above to play!*")
    elif status == "won_player":
        winner = state.get("winner", "Visitor")
        md.append(f"**Status:** 🏆 **VICTORY!** [@{winner}](https://github.com/{winner}) triumphed over Aadarsh-AI! (+20 pts)")
    elif status == "won_ai":
        md.append("**Status:** 🤖 **Aadarsh-AI won!** Better luck next round!")
    else:
        md.append("**Status:** 🤝 **It's a DRAW!** Well defended!")

    md.append(f"**Last Turn:** {last_move}\n")

    reset_url = issue_url(
        "arcade:ttt:new",
        "Click 'Submit new issue' to start a fresh Tic-Tac-Toe match!"
    )
    md.append(f"[ 🔄 Start New Tic-Tac-Toe Game ]({reset_url})\n")

    return "\n".join(md)
