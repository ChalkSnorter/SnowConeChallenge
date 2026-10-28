"""Builds index.html: a snow cone page hiding an invisible, computed program.

Design (v2):
  * The payload is a *real* Whitespace-style program (stack, heap, loop, labels)
    written in three invisible zero-width characters instead of space/tab/LF.
  * The flag is never present as data: only (char + key) values are stored,
    and the program derives each key in a loop, so it must actually be run.
  * Two extra invisible characters are sprinkled in as noise.
  * Payload is scattered across <title>, <h1>, <p> and every recipe line.
"""
import random

FLAG = "flag{sn0w_c0n3_z3r0_w1dth}"

# Which invisible char plays S / T / L. (Players must work this out: 6 options.)
MAP = {"S": "\u200c", "T": "\u200b", "L": "\u200d"}
NOISE = ["\u2060", "\ufeff"]
NOISE_RATE = 0.06
rng = random.Random(1337)


def num(n):
    return ("S" if n >= 0 else "T") + bin(abs(n))[2:].replace("0", "S").replace("1", "T") + "L"

def lab(name):
    return name + "L"

PUSH = lambda n: "SS" + num(n)
COPY = lambda n: "STS" + num(n)
DUP, SWAP, DISCARD = "SLS", "SLT", "SLL"
ADD, SUB, MUL, MOD = "TSSS", "TSST", "TSSL", "TSTT"
STORE, RETR = "TTS", "TTT"
MARK = lambda l: "LSS" + lab(l)
JUMP = lambda l: "LSL" + lab(l)
JZ = lambda l: "LTS" + lab(l)
PRINTC, END = "TLSS", "LLL"

def key(i):
    return (3 * i * i + 7 * i + 11) % 97

LOOP, DONE = "STSTTS", "TTSSTS"
n = len(FLAG)

prog = ""
for i, c in enumerate(FLAG):               # heap[i] = ord(c) + key(i)
    prog += PUSH(i) + PUSH(ord(c) + key(i)) + STORE
prog += PUSH(0)                            # loop counter on the stack
prog += MARK(LOOP)
prog += DUP + PUSH(n) + SUB + JZ(DONE)     # leave when i == n
prog += DUP + DUP + MUL + PUSH(3) + MUL + PUSH(11) + ADD   # 3i^2 + 11
prog += COPY(1) + PUSH(7) + MUL + ADD      # + 7i
prog += PUSH(97) + MOD                     # key
prog += COPY(1) + RETR + SWAP + SUB + PRINTC   # print heap[i] - key
prog += PUSH(1) + ADD + JUMP(LOOP)
prog += MARK(DONE) + DISCARD + END

stream = ""
for ch in prog:
    stream += MAP[ch]
    if rng.random() < NOISE_RATE:
        stream += rng.choice(NOISE)

title = "Secret Snow Cone Recipe"
h1 = "&#127847; Snow Cone Corner"
intro = "Our family recipe, finally shared."
recipe = [
    "Grandma's Secret Snow Cone Recipe",
    "Ingredients: 2 cups shaved ice, 1/2 cup sugar, 1 cup water, a few drops of food coloring.",
    "Step 1: Dissolve the sugar in warm water, then stir in the food coloring.",
    "Step 2: Chill the syrup in the fridge for 30 minutes.",
    "Step 3: Pack the shaved ice into a paper cup.",
    "Step 4: Pour the syrup slowly over the ice.",
    "Step 5: Serve immediately with a spoon-straw.",
]
carriers = 3 + len(recipe)
size = -(-len(stream) // carriers)
chunks = [stream[i * size:(i + 1) * size] for i in range(carriers)]
t, h, p, *r = [x + c for x, c in zip([title, h1, intro] + recipe, chunks)]

html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<title>{t}</title>'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<style>body{font-family:Georgia,serif;max-width:640px;margin:3rem auto;padding:0 1rem;'
        'background:#eef7fb;color:#12303f;line-height:1.6}'
        'h1{color:#d6336c}.recipe{background:#fff;padding:1.5rem;border-radius:12px;'
        'box-shadow:0 2px 8px #0002}</style></head><body>'
        f'<h1>{h}</h1><p>{p}</p>'
        '<div class="recipe">' + "<br>".join(r) + '</div></body></html>')
open("index.html", "w", encoding="utf-8", newline="").write(html)
print("wrote index.html,", len(stream), "invisible chars hidden")
