"""
Master Arcade Engine for sudo-aadarsh's GitHub Profile.
Routes issue commands, updates game states, awards leaderboard points,
rebuilds README.md, and posts feedback to GitHub issues.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error

# Add games directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

import connect4
import tictactoe
import chess_game
import wordle
import leaderboard

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
REPO_OWNER = "sudo-aadarsh"
REPO_NAME = "sudo-aadarsh"


def post_github_issue_reply_and_close(issue_number: str, message: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token or not issue_number or not issue_number.isdigit():
        print(f"[Info] Skipping issue comment (token or valid issue number not present: {issue_number})")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Aadarsh-Arcade-Bot"
    }

    # 1. Post Comment
    comment_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
    comment_body = json.dumps({
        "body": f"{message}\n\n👉 [View the updated board & live leaderboard on Profile](https://github.com/{REPO_OWNER}/{REPO_NAME})"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(comment_url, data=comment_body, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            print(f"[Success] Comment posted to issue #{issue_number} (status {resp.status})")
    except Exception as e:
        print(f"[Warning] Failed to post comment to issue: {e}")

    # 2. Close Issue
    close_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    close_body = json.dumps({"state": "closed", "state_reason": "completed"}).encode("utf-8")

    try:
        req = urllib.request.Request(close_url, data=close_body, headers=headers, method="PATCH")
        with urllib.request.urlopen(req) as resp:
            print(f"[Success] Issue #{issue_number} closed successfully (status {resp.status})")
    except Exception as e:
        print(f"[Warning] Failed to close issue: {e}")


def build_arcade_markdown() -> str:
    banner_url = "assets/arcade-banner.svg"

    lines = [
        "<!-- ARCADE:START -->",
        f'<p align="center">',
        f'  <img src="{banner_url}" alt="Aadarsh\'s Cyber Arcade" width="850"/>',
        f'</p>\n',
        '<p align="center">',
        '  <a href="#-game-1-connect-four-vs-aadarsh-ai"><b>🟡 Connect Four</b></a> &nbsp;•&nbsp;',
        '  <a href="#-game-2-tic-tac-toe-vs-aadarsh-ai"><b>❌ Tic-Tac-Toe</b></a> &nbsp;•&nbsp;',
        '  <a href="#-game-3-community-chess-vs-aadarsh-ai"><b>♟️ Chess</b></a> &nbsp;•&nbsp;',
        '  <a href="#-game-4-developer-wordle"><b>🟩 Dev Wordle</b></a> &nbsp;•&nbsp;',
        '  <a href="#-hall-of-fame--community-leaderboard"><b>🏆 Hall of Fame</b></a>',
        '</p>\n',
        '> 💡 **How it works:** Click any move or button below to submit your turn via a pre-filled GitHub Issue. Our GitHub Actions engine parses your move in real time, executes the AI response, and updates the board right here within seconds! 🚀\n',
        "---",
        connect4.render_markdown(),
        "---",
        tictactoe.render_markdown(),
        "---",
        chess_game.render_markdown(),
        "---",
        wordle.render_markdown(),
        "---",
        leaderboard.render_markdown(),
        "<!-- ARCADE:END -->"
    ]
    return "\n".join(lines)


def update_readme() -> None:
    arcade_content = build_arcade_markdown()

    if os.path.exists(README_PATH):
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r"<!-- ARCADE:START -->.*?<!-- ARCADE:END -->"
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, arcade_content, content, flags=re.DOTALL)
        else:
            # Preserve header/footer elements if desired, or replace the entire file with our rich profile
            # Let's check what existing elements to preserve (e.g. contribution snake, developer info)
            snake_part = ""
            if "## 🐍 Contribution Snake" in content:
                snake_part = content[content.find("## 🐍 Contribution Snake"):]
            
            new_content = f"{arcade_content}\n\n---\n\n{snake_part}" if snake_part else arcade_content
    else:
        new_content = arcade_content

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[Success] README.md successfully updated with latest arcade state!")


def process_command(title: str, username: str) -> str:
    title = title.strip()
    norm = title.lower()

    # 1. Connect Four
    if norm.startswith("arcade:c4:drop:"):
        match = re.search(r"arcade:c4:drop:(\d+)", norm)
        if match:
            col = int(match.group(1))
            success, msg, pts, won, draw = connect4.process_move(col, username)
            if success:
                award_msg = leaderboard.award_player(username, pts, "connect4", won=won, draw=draw)
                return f"{msg}\n\n{award_msg}"
            return f"⚠️ {msg}"
    elif norm in ["arcade:c4:new", "arcade:c4:reset"]:
        return connect4.reset_game()

    # 2. Tic-Tac-Toe
    elif norm.startswith("arcade:ttt:move:"):
        match = re.search(r"arcade:ttt:move:(\d+),(\d+)", norm)
        if match:
            r, c = int(match.group(1)), int(match.group(2))
            success, msg, pts, won, draw = tictactoe.process_move(r, c, username)
            if success:
                award_msg = leaderboard.award_player(username, pts, "tictactoe", won=won, draw=draw)
                return f"{msg}\n\n{award_msg}"
            return f"⚠️ {msg}"
    elif norm in ["arcade:ttt:new", "arcade:ttt:reset"]:
        return tictactoe.reset_game()

    # 3. Chess
    elif norm.startswith("arcade:chess:move:"):
        move_str = title.split("arcade:chess:move:", 1)[1].strip()
        success, msg, pts, won, draw = chess_game.process_move(move_str, username)
        if success:
            award_msg = leaderboard.award_player(username, pts, "chess", won=won, draw=draw)
            return f"{msg}\n\n{award_msg}"
        return f"⚠️ {msg}"
    elif norm in ["arcade:chess:new", "arcade:chess:reset"]:
        return chess_game.reset_game()

    # 4. Wordle
    elif norm.startswith("arcade:wordle:guess:"):
        guess_str = title.split("arcade:wordle:guess:", 1)[1].strip()
        success, msg, pts, won, lost = wordle.process_guess(guess_str, username)
        if success:
            award_msg = leaderboard.award_player(username, pts, "wordle", won=won, draw=False)
            return f"{msg}\n\n{award_msg}"
        return f"⚠️ {msg}"
    elif norm in ["arcade:wordle:new", "arcade:wordle:reset"]:
        return wordle.reset_game()

    # 5. Global reset / admin
    elif norm in ["arcade:reset:all", "--reset-all"]:
        connect4.reset_game()
        tictactoe.reset_game()
        chess_game.reset_game()
        wordle.reset_game()
        return "All 4 games have been reset to initial state!"

    elif norm in ["--render-only", "arcade:render"]:
        return "Arcade rendered."

    return f"Unrecognized arcade command: `{title}`"


def main():
    if len(sys.argv) < 2:
        print("Usage: python games/engine.py <issue_title> [username] [issue_number]")
        print("Rendering arcade with current state...")
        update_readme()
        return

    issue_title = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "Challenger"
    issue_number = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"[Arcade Engine] Executing '{issue_title}' for @{username} (Issue #{issue_number})...")
    result_msg = process_command(issue_title, username)
    print(f"[Arcade Engine] Result: {result_msg}")

    update_readme()

    if issue_number:
        post_github_issue_reply_and_close(issue_number, result_msg)


if __name__ == "__main__":
    main()
