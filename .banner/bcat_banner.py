import sys
import time
import random
import shutil

TEXT = '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠉⠉⠻⣷⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⠀⠛⠛⠁⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠀⠀⠀⢀⣤⠤⣤⡀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣘⣷⣀⠀⢀⠏⠀⠀⣈⡇\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢾⠋⠁⠀⠀⠉⠙⢷⣼⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠈⠑⠃⣠⠀⠀⠀⠀⠙⣿⡄⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣄⡀⣠⠟⠁⣠⠄⠤⣄⠘⣷⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠙⣆⣿⡄⠀⠀\n⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⡄⣿⣿⠃⠀⠀\n⡔⠉⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⢬⣿⣿⣿⡀⠀⠀\n⣇⠀⠀⠀⡤⠤⣄⠀⠀⡴⢲⡆⠀⠀⠀⠀⠀⣠⣾⣿⣎⢸⣿⣿⣿⣿⣧⠀\n⠸⢦⡀⢸⡁⠺⠋⠀⠈⣧⠀⠁⠀⢼⣤⣀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n⠀⠈⠛⢦⣷⣤⣸⣧⣤⣨⣽⣶⠶⢚⣿⠟⢻⣿⡏⠀⢉⣿⠁⠉⠙⣿⡿⠀\n⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⣼⠁⣠⣄⠻⢷⣾⡟⢻⣤⣤⣼⡿⠁⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣄⣉⣼⠇⢸⣻⢟⡿⢻⡏⠁⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠈⠈⠀⠈⠀⠀⠀⠀⠀'
PALETTE = ['32']
ANIMATION = 'Glitch'
BUDGET = 0.5  # total animation time in seconds (kept short on purpose)

ESC = "\x1b"
RESET = ESC + "[0m"
NOISE = "#@$%&*+=?"


def out(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def get_lines():
    cols = shutil.get_terminal_size((80, 24)).columns - 1
    return [l.rstrip().expandtabs(4)[:cols] for l in TEXT.splitlines()]


def color(i, total):
    return ESC + "[" + PALETTE[i * len(PALETTE) // max(total, 1)] + "m"


def instant(lines):
    n = len(lines)
    out("\n".join(color(i, n) + l + RESET for i, l in enumerate(lines)) + "\n")


def cascade(lines):
    n = len(lines)
    delay = BUDGET / max(n, 1)
    for i, l in enumerate(lines):
        out(color(i, n) + l + RESET + "\n")
        time.sleep(delay)


def typewriter(lines):
    n = len(lines)
    total = sum(len(l) for l in lines) or 1
    step = max(1, total // 250)
    delay = BUDGET / max(total / step, 1)
    for i, l in enumerate(lines):
        out(color(i, n))
        for k in range(0, len(l), step):
            out(l[k:k + step])
            time.sleep(delay)
        out(RESET + "\n")


def glitch(lines):
    n = len(lines)
    delay = BUDGET / (max(n, 1) * 3)
    for i, l in enumerate(lines):
        c = color(i, n)
        if l.strip():
            for _ in range(2):
                noisy = "".join(
                    random.choice(NOISE) if ch != " " and random.random() < 0.5 else ch
                    for ch in l
                )
                out(c + noisy + RESET + "\r")
                time.sleep(delay)
        out(c + l + RESET + "\n")
        time.sleep(delay)


def center(lines):
    n = len(lines)
    frames = 8
    delay = BUDGET / (max(n, 1) * frames)
    for i, l in enumerate(lines):
        c = color(i, n)
        mid = len(l) // 2
        if l.strip():
            for f in range(1, frames):
                half = (len(l) // 2) * f // frames
                left = max(0, mid - half)
                right = min(len(l), mid + half + 1)
                out(c + " " * left + l[left:right] + RESET + "\r")
                time.sleep(delay)
        out(c + l + RESET + "\n")


ANIMS = {
    "Typewriter": typewriter,
    "Line Cascade": cascade,
    "Center Reveal": center,
    "Glitch": glitch,
}


def main():
    if not sys.stdout.isatty():
        return
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    lines = get_lines()
    out(ESC + "[2J" + ESC + "[H" + ESC + "[?25l")
    try:
        ANIMS.get(ANIMATION, instant)(lines)
    except KeyboardInterrupt:
        pass
    finally:
        out(RESET + ESC + "[?25h")


if __name__ == "__main__":
    main()
