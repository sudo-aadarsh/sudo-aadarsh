"""
Connect Four Game Engine for GitHub Profile Arcade.
Grid: 6 rows x 7 cols.
Player: 🟡 (Visitor) | AI: 🔵 (Aadarsh-AI) | Empty: ⚪
"""

import json
import os
import random
from typing import Dict, Any, Tuple, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "connect4.json")
REPO_OWNER = "sudo-aadarsh"
REPO_NAME = "sudo-aadarsh"

ROWS = 6
COLS = 7


def issue_url(title: str, body: str) -> str:
    from urllib.parse import quote_plus
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?title={quote_plus(title)}&body={quote_plus(body)}"


def default_state() -> Dict[str, Any]:
    return {
        "board": [[0 for _ in range(COLS)] for _ in range(ROWS)],
        "status": "in_progress",  # "in_progress", "won_player", "won_ai", "draw"
        "last_player": None,
        "winner": None,
        "last_move": None,
        "turn_count": 0
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


def check_win(board: list, piece: int) -> bool:
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Diagonal Positive
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Diagonal Negative
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False


def is_board_full(board: list) -> bool:
    return all(board[0][c] != 0 for c in range(COLS))


def get_available_row(board: list, col: int) -> Optional[int]:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None


def get_valid_cols(board: list) -> list:
    return [c for c in range(COLS) if board[0][c] == 0]


def choose_ai_move(board: list) -> Optional[int]:
    valid_cols = get_valid_cols(board)
    if not valid_cols:
        return None

    # 1. Can AI win immediately?
    for c in valid_cols:
        r = get_available_row(board, c)
        board[r][c] = 2
        if check_win(board, 2):
            board[r][c] = 0
            return c
        board[r][c] = 0

    # 2. Block player immediate win
    for c in valid_cols:
        r = get_available_row(board, c)
        board[r][c] = 1
        if check_win(board, 1):
            board[r][c] = 0
            return c
        board[r][c] = 0

    # 3. Avoid moves that let player win on the next turn right above
    safe_cols = []
    for c in valid_cols:
        r = get_available_row(board, c)
        board[r][c] = 2
        safe = True
        if r - 1 >= 0:
            board[r - 1][c] = 1
            if check_win(board, 1):
                safe = False
            board[r - 1][c] = 0
        board[r][c] = 0
        if safe:
            safe_cols.append(c)

    candidate_cols = safe_cols if safe_cols else valid_cols

    # Prefer center columns: col 3, then 2,4, then 1,5, then 0,6
    preference = [3, 2, 4, 1, 5, 0, 6]
    for c in preference:
        if c in candidate_cols:
            return c

    return random.choice(candidate_cols)


def process_move(col: int, username: str) -> Tuple[bool, str, int, bool, bool]:
    """
    Processes a drop move in column `col` (0-indexed).
    Returns (success, message, points_earned, won, draw).
    """
    state = load_state()

    if state["status"] != "in_progress":
        return False, "This game is already completed! Click [Start New Game] to begin another match.", 0, False, False

    if col < 0 or col >= COLS:
        return False, f"Invalid column {col}. Column must be between 1 and {COLS}.", 0, False, False

    board = state["board"]
    row = get_available_row(board, col)
    if row is None:
        return False, f"Column {col + 1} is already full! Please pick another column.", 0, False, False

    # Player 1 (Visitor) drop
    board[row][col] = 1
    state["last_player"] = username
    state["turn_count"] = state.get("turn_count", 0) + 1
    state["last_move"] = f"@{username} dropped in Column {col + 1}"

    # Check if player won
    if check_win(board, 1):
        state["status"] = "won_player"
        state["winner"] = username
        save_state(state)
        return True, f"🎉 CONNECT FOUR! @{username} won the match!", 30, True, False

    # Check draw
    if is_board_full(board):
        state["status"] = "draw"
        save_state(state)
        return True, f"🤝 Board is full! Connect Four ended in a DRAW.", 10, False, True

    # AI Turn
    ai_col = choose_ai_move(board)
    if ai_col is not None:
        ai_row = get_available_row(board, ai_col)
        board[ai_row][ai_col] = 2
        state["last_move"] += f" | Aadarsh-AI countered in Column {ai_col + 1}"

        if check_win(board, 2):
            state["status"] = "won_ai"
            state["winner"] = "Aadarsh-AI"
            save_state(state)
            return True, f"🤖 Aadarsh-AI got 4-in-a-row! Good try @{username}!", 2, False, False

        if is_board_full(board):
            state["status"] = "draw"
            save_state(state)
            return True, f"🤝 Board is full! Connect Four ended in a DRAW.", 10, False, True

    save_state(state)
    return True, f"Move accepted in Column {col + 1}! Aadarsh-AI made its counter-move.", 2, False, False


def reset_game() -> str:
    state = default_state()
    save_state(state)
    return "Connect Four has been reset! A new game is ready."


def render_markdown() -> str:
    state = load_state()
    board = state["board"]
    status = state["status"]
    last_move = state.get("last_move", "No moves yet.")

    piece_map = {0: "⚪", 1: "🟡", 2: "🔵"}

    md = []
    md.append("### 🟡 Game 1: Connect Four vs Aadarsh-AI")
    md.append("> **Rules:** Align 4 yellow tokens (🟡) horizontally, vertically, or diagonally before Aadarsh-AI (🔵) blocks you!\n")

    # Drop buttons row
    if status == "in_progress":
        drop_links = []
        for c in range(COLS):
            if board[0][c] == 0:
                url = issue_url(
                    f"arcade:c4:drop:{c}",
                    f"Just click 'Submit new issue' to drop your token in Column {c + 1}!\n\n*(Automated turn for @sudo-aadarsh's arcade)*"
                )
                drop_links.append(f"[ ⬇️ Col {c + 1} ]({url})")
            else:
                drop_links.append("🚫 Full")
        md.append("| " + " | ".join(drop_links) + " |")
    else:
        headers = [f"Col {c + 1}" for c in range(COLS)]
        md.append("| " + " | ".join(headers) + " |")

    md.append("| " + " | ".join([":---:"] * COLS) + " |")

    # Render board rows
    for r in range(ROWS):
        row_str = " | ".join(piece_map[board[r][c]] for c in range(COLS))
        md.append(f"| {row_str} |")

    # Status line
    md.append("")
    if status == "in_progress":
        md.append(f"**Status:** 🟡 **Visitor's Turn** vs 🔵 **Aadarsh-AI** &nbsp;|&nbsp; *Click any `⬇️ Col` button above to drop!*")
    elif status == "won_player":
        winner = state.get("winner", "Visitor")
        md.append(f"**Status:** 🏆 **VICTORY!** [@{winner}](https://github.com/{winner}) connected four and defeated Aadarsh-AI! (+30 pts)")
    elif status == "won_ai":
        md.append("**Status:** 🤖 **Aadarsh-AI won this match!** Better luck next round!")
    else:
        md.append("**Status:** 🤝 **It's a DRAW!** The grid is full.")

    md.append(f"**Last Turn:** {last_move}\n")

    reset_url = issue_url(
        "arcade:c4:new",
        "Click 'Submit new issue' to start a fresh Connect Four game!"
    )
    md.append(f"[ 🔄 Start New Connect Four Game ]({reset_url})\n")

    return "\n".join(md)
