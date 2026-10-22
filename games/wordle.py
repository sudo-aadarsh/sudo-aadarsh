"""
Developer Wordle Engine for GitHub Profile Arcade.
6 guesses to find the secret 5-letter tech word.
Feedback: 🟩 (exact match), 🟨 (misplaced), ⬛ (not in word).
"""

import json
import os
import random
from typing import Dict, Any, Tuple, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "wordle.json")
REPO_OWNER = "sudo-aadarsh"
REPO_NAME = "sudo-aadarsh"

TECH_WORDS = [
    "REACT", "LINUX", "REDIS", "ASYNC", "STACK", "CLONE", "PROXY", "NEXUS",
    "ARRAY", "BUILD", "QUERY", "CACHE", "TOKEN", "GRAPH", "ROBOT", "LOGIC",
    "SPARK", "KAFKA", "SWIFT", "SHELL", "BYTES", "PATCH", "CLOUD", "FLOAT",
    "INDEX", "MACRO", "PARSE", "PIPES", "QUEUE", "ROUTE", "SCALE", "SCOPE",
    "TABLE", "YIELD", "AGILE", "BENCH", "BLOCK", "CRASH", "FETCH", "FLASK",
    "HOOKS", "MODEL", "MUTEX", "OAUTH", "PANEL", "REGEX", "RESET", "SHARD",
    "TESTS", "VALID", "WHILE", "CONST", "DEBUG", "EVENT", "INPUT", "MUTAT"
]


def issue_url(title: str, body: str) -> str:
    from urllib.parse import quote_plus
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?title={quote_plus(title)}&body={quote_plus(body)}"


def default_state() -> Dict[str, Any]:
    return {
        "target_word": random.choice(TECH_WORDS),
        "guesses": [],
        "status": "in_progress",
        "winner": None,
        "max_attempts": 6
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


def evaluate_guess(target: str, guess: str) -> List[str]:
    result = ["⬛"] * 5
    target_chars = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "🟩"
            target_chars[i] = None

    for i in range(5):
        if result[i] != "🟩" and guess[i] in target_chars:
            result[i] = "🟨"
            target_chars[target_chars.index(guess[i])] = None

    return result


def process_guess(guess_str: str, username: str) -> Tuple[bool, str, int, bool, bool]:
    state = load_state()

    if state["status"] != "in_progress":
        return False, f"This Wordle puzzle is already finished! Click [Start New Wordle] to play a new word.", 0, False, False

    clean_guess = guess_str.strip().upper()
    if len(clean_guess) != 5 or not clean_guess.isalpha():
        return False, f"Invalid guess `{guess_str}`! Guesses must be exactly 5 letters (A-Z).", 0, False, False

    existing_guesses = [g["word"] for g in state.get("guesses", [])]
    if clean_guess in existing_guesses:
        return False, f"The word `{clean_guess}` was already guessed! Try another word.", 0, False, False

    target = state["target_word"]
    colors = evaluate_guess(target, clean_guess)
    guesses = state.setdefault("guesses", [])
    guesses.append({
        "word": clean_guess,
        "colors": colors,
        "user": username
    })

    if clean_guess == target:
        state["status"] = "won"
        state["winner"] = username
        attempt_num = len(guesses)
        bonus = (6 - attempt_num) * 3
        points = 25 + bonus
        save_state(state)
        return True, f"🎯 INCREDIBLE! @{username} cracked the Dev Wordle in {attempt_num}/6 tries! The word was **{target}**! (+{points} pts)", points, True, False

    if len(guesses) >= state["max_attempts"]:
        state["status"] = "lost"
        save_state(state)
        return True, f"💀 Out of attempts! The secret word was **{target}**. Nice try @{username}!", 3, False, True

    save_state(state)
    return True, f"Guess `{clean_guess}` accepted! ({len(guesses)}/6 attempts used).", 3, False, False


def reset_game() -> str:
    state = default_state()
    save_state(state)
    return "A new Developer Wordle puzzle has been selected! Start guessing."


def render_markdown() -> str:
    state = load_state()
    guesses = state.get("guesses", [])
    status = state.get("status", "in_progress")
    target = state.get("target_word", "REACT")

    md = []
    md.append("### 🟩 Game 4: Developer Wordle")
    md.append("> **Goal:** Guess the secret 5-letter software engineering term in 6 tries! Feedback: 🟩 Correct spot, 🟨 Wrong spot, ⬛ Not in word.\n")

    md.append('<div align="center">\n')
    md.append("| 1️⃣ | 2️⃣ | 3️⃣ | 4️⃣ | 5️⃣ | Challenger |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :--- |")

    for i in range(6):
        if i < len(guesses):
            g = guesses[i]
            w = g["word"]
            c = g["colors"]
            u = g.get("user", "player")
            cells = [f"{c[j]} **{w[j]}**" for j in range(5)]
            md.append(f"| {' | '.join(cells)} | [@{u}](https://github.com/{u}) |")
        else:
            empty_cells = ["⬜ ` `"] * 5
            md.append(f"| {' | '.join(empty_cells)} | *Empty* |")

    md.append("\n</div>\n")

    # Keyboard tracker
    used_letters = {}
    for g in guesses:
        for idx, char in enumerate(g["word"]):
            col = g["colors"][idx]
            if col == "🟩":
                used_letters[char] = "🟩"
            elif col == "🟨" and used_letters.get(char) != "🟩":
                used_letters[char] = "🟨"
            elif col == "⬛" and char not in used_letters:
                used_letters[char] = "⬛"

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    kb_display = [f"`{char}`{used_letters.get(char, '⚪')}" for char in alphabet]

    md.append("<details>")
    md.append("<summary><b>🔤 Alphabet Key Status</b> (Click to inspect available letters)</summary>\n")
    md.append('<p align="center">\n')
    md.append(" &nbsp; ".join(kb_display[:13]) + "<br/><br/>" + " &nbsp; ".join(kb_display[13:]) + "\n")
    md.append("</p>\n")
    md.append("</details>\n")

    if status == "in_progress":
        guess_url = issue_url(
            "arcade:wordle:guess:REACT",
            "Replace 'REACT' in the issue title above with your 5-letter tech guess (e.g. LINUX, REDIS, ASYNC, STACK, CLOUD) and submit!"
        )
        md.append('<div align="center">\n')
        md.append(f"[ 🎯 Click Here to Submit a 5-Letter Word Guess ]({guess_url})\n")

        if len(guesses) < 2:
            quick_suggestions = [w for w in ["REACT", "LINUX", "ASYNC", "REDIS"] if w not in [g["word"] for g in guesses]]
            quick_btns = []
            for sw in quick_suggestions[:3]:
                s_url = issue_url(f"arcade:wordle:guess:{sw}", f"Click 'Submit new issue' to guess `{sw}`!")
                quick_btns.append(f"[`{sw}`]({s_url})")
            md.append(f"💡 **Suggested Starters:** " + " &nbsp;|&nbsp; ".join(quick_btns) + "\n")

        attempts_left = 6 - len(guesses)
        md.append(f"**Attempts Remaining:** ⏳ **{attempts_left} / 6**\n")
        md.append("</div>\n")
    elif status == "won":
        winner = state.get("winner", "Someone")
        md.append(f"**Status:** 🎉 **SOLVED!** [@{winner}](https://github.com/{winner}) cracked the word **{target}**! (+Bonus pts)\n")
    else:
        md.append(f"**Status:** 💀 **Game Over!** The word was **{target}**.\n")

    reset_url = issue_url(
        "arcade:wordle:new",
        "Click 'Submit new issue' to generate a fresh Wordle puzzle!"
    )
    md.append(f"[ 🔄 Start New Wordle Puzzle ]({reset_url})\n")

    return "\n".join(md)
