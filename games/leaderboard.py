"""
Leaderboard and Player Profile Manager for GitHub Profile Arcade.
Tracks scores, wins, streaks, badges, and recent activity.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "leaderboard.json")


def load_leaderboard() -> Dict[str, Any]:
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "players": {},
        "total_moves": 0,
        "recent_activity": []
    }


def save_leaderboard(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def award_player(username: str, points: int, game_name: str, won: bool = False, draw: bool = False) -> str:
    """Awards points, updates win streak and badges for a player."""
    data = load_leaderboard()
    players = data.setdefault("players", {})
    username = username.strip().lstrip("@")

    if username not in players:
        players[username] = {
            "score": 0,
            "wins": {"connect4": 0, "tictactoe": 0, "chess": 0, "wordle": 0},
            "games_played": 0,
            "streak": 0,
            "favorite_game": game_name,
            "last_active": datetime.utcnow().strftime("%Y-%m-%d"),
            "badges": []
        }

    p = players[username]
    p["score"] += points
    p["games_played"] += 1
    p["last_active"] = datetime.utcnow().strftime("%Y-%m-%d")

    if won:
        p["wins"][game_name] = p["wins"].get(game_name, 0) + 1
        p["streak"] += 1
    elif not draw:
        p["streak"] = 0

    # Badges evaluation
    badges = set(p.get("badges", []))
    if p["wins"].get("chess", 0) >= 1:
        badges.add("👑 Grandmaster")
    if p["wins"].get("wordle", 0) >= 1:
        badges.add("⚡ Wordle Wizard")
    if p["wins"].get("connect4", 0) >= 1:
        badges.add("🎯 Tactician")
    if p["wins"].get("tictactoe", 0) >= 1:
        badges.add("🤖 AI Slayer")
    if p["streak"] >= 3:
        badges.add("🔥 On Fire")
    if p["score"] >= 100:
        badges.add("💎 Century Club")
    p["badges"] = sorted(list(badges))

    # Update favorite game
    fav_game = max(p["wins"].items(), key=lambda item: item[1])[0] if any(p["wins"].values()) else game_name
    p["favorite_game"] = fav_game

    data["total_moves"] = data.get("total_moves", 0) + 1
    
    # Record recent activity
    action_text = f"won {game_name}" if won else ("drew" if draw else f"played {game_name}")
    recent = data.setdefault("recent_activity", [])
    recent.insert(0, {
        "user": username,
        "action": action_text,
        "pts": points,
        "time": datetime.utcnow().strftime("%b %d, %H:%M UTC")
    })
    data["recent_activity"] = recent[:8]  # keep last 8

    save_leaderboard(data)
    return f"🌟 @{username} gained **+{points} pts**! Total score: **{p['score']} pts**."


def render_leaderboard_markdown() -> str:
    data = load_leaderboard()
    players = data.get("players", {})
    
    sorted_players = sorted(
        players.items(),
        key=lambda item: (item[1].get("score", 0), item[1].get("streak", 0)),
        reverse=True
    )

    total_players = len(players)
    total_moves = data.get("total_moves", 0)
    top_champion = sorted_players[0][0] if sorted_players else "sudo-aadarsh"

    md = [
        "### 🏆 Hall of Fame & Community Leaderboard\n",
        f"> **Arcade Stats:** 👥 **{total_players}** Active Players &nbsp;|&nbsp; 🕹️ **{total_moves}** Total Turns Played &nbsp;|&nbsp; 👑 Current Champion: **[@{top_champion}](https://github.com/{top_champion})**\n",
        "| Rank | Challenger | Total Score | Games Won | Current Streak | Badges |",
        "| :---: | :--- | :---: | :---: | :---: | :--- |"
    ]

    if not sorted_players:
        md.append("| 🥇 1 | [@sudo-aadarsh](https://github.com/sudo-aadarsh) | 100 pts | 4 wins | 🔥 3 | 👑 Grandmaster, ⚡ Wordle Wizard |")
        md.append("| 🥈 2 | *Open for Challengers* | 0 pts | 0 wins | 0 | 🎯 Play any game above to claim your spot! |")
    else:
        rank_icons = ["🥇 1", "🥈 2", "🥉 3"]
        for idx, (uname, info) in enumerate(sorted_players[:10]):
            rank_str = rank_icons[idx] if idx < 3 else f"#{idx + 1}"
            total_wins = sum(info.get("wins", {}).values())
            streak_str = f"🔥 {info.get('streak', 0)}" if info.get('streak', 0) > 0 else "0"
            badge_list = info.get("badges", [])
            badge_str = ", ".join(badge_list[:3]) if badge_list else "🌱 Rookie"
            md.append(f"| {rank_str} | [@{uname}](https://github.com/{uname}) | **{info.get('score', 0)} pts** | {total_wins} | {streak_str} | {badge_str} |")

    md.append("\n<details>")
    md.append("<summary><b>📜 Scoring Rules & How to Earn Points</b></summary>\n")
    md.append("- 🎯 **Connect Four:** Win = **+30 pts** | Move = **+2 pts** | Draw = **+10 pts**")
    md.append("- ❌ **Tic-Tac-Toe:** Win = **+20 pts** | Move = **+1 pt** | Draw = **+5 pts**")
    md.append("- ♟️ **Chess:** Win = **+50 pts** | Valid Move = **+2 pts** | Draw = **+15 pts**")
    md.append("- 🟩 **Developer Wordle:** Solved = **+25 pts** (+Bonus for fewer tries) | Valid Guess = **+3 pts**")
    md.append("- 🏅 **Streaks:** Win multiple games in a row to earn the **🔥 On Fire** badge!")
    md.append("</details>\n")

    return "\n".join(md)


render_markdown = render_leaderboard_markdown

