"""Reference solve: python3 solve.py [index.html | http://host/]
Pulls every zero-width char in document order, tries the 6 S/T/L assignments of
the three most frequent ones (the other two are noise), and runs a full
Whitespace interpreter (stack, heap, labels, arithmetic) on each."""
import sys, itertools, urllib.request
from collections import Counter

ZW = set("\u200b\u200c\u200d\u2060\ufeff")

def fetch(src):
    if src.startswith("http"):
        return urllib.request.urlopen(src).read().decode("utf-8")
    return open(src, encoding="utf-8", newline="").read()

def parse(code):
    i, ops, labels = 0, [], {}
    def num():
        nonlocal i
        sign = -1 if code[i] == "T" else 1; i += 1
        v = 0
        while code[i] != "L":
            v = v * 2 + (code[i] == "T"); i += 1
        i += 1
        return sign * v
    def label():
        nonlocal i
        j = code.index("L", i); s = code[i:j]; i = j + 1
        return s
    table = {
        "SS": ("push", num), "STS": ("copy", num), "STL": ("slide", num),
        "SLS": ("dup", None), "SLT": ("swap", None), "SLL": ("pop", None),
        "TSSS": ("add", None), "TSST": ("sub", None), "TSSL": ("mul", None),
        "TSTS": ("div", None), "TSTT": ("mod", None),
        "TTS": ("store", None), "TTT": ("retr", None),
        "LSS": ("mark", label), "LST": ("call", label), "LSL": ("jmp", label),
        "LTS": ("jz", label), "LTT": ("jn", label), "LTL": ("ret", None),
        "LLL": ("end", None),
        "TLSS": ("outc", None), "TLST": ("outn", None),
    }
    while i < len(code):
        for ln in (2, 3, 4):
            if code[i:i + ln] in table:
                name, arg = table[code[i:i + ln]]; i += ln
                a = arg() if arg else None
                if name == "mark": labels[a] = len(ops)
                ops.append((name, a)); break
        else:
            raise ValueError("bad op")
    return ops, labels

def run(code, limit=200000):
    ops, labels = parse(code)
    st, heap, calls, out, pc, steps = [], {}, [], [], 0, 0
    while pc < len(ops) and steps < limit:
        steps += 1
        op, a = ops[pc]; pc += 1
        if op == "push": st.append(a)
        elif op == "copy": st.append(st[-1 - a])
        elif op == "slide": top = st.pop(); del st[-a:]; st.append(top)
        elif op == "dup": st.append(st[-1])
        elif op == "swap": st[-1], st[-2] = st[-2], st[-1]
        elif op == "pop": st.pop()
        elif op in ("add", "sub", "mul", "div", "mod"):
            b, x = st.pop(), st.pop()
            st.append({"add": x + b, "sub": x - b, "mul": x * b,
                       "div": x // b if b else 0, "mod": x % b if b else 0}[op])
        elif op == "store": v, ad = st.pop(), st.pop(); heap[ad] = v
        elif op == "retr": st.append(heap[st.pop()])
        elif op == "call": calls.append(pc); pc = labels[a]
        elif op == "jmp": pc = labels[a]
        elif op == "jz":
            if st.pop() == 0: pc = labels[a]
        elif op == "jn":
            if st.pop() < 0: pc = labels[a]
        elif op == "ret": pc = calls.pop()
        elif op == "outc": out.append(chr(st.pop()))
        elif op == "outn": out.append(str(st.pop()))
        elif op == "end": break
    return "".join(out)

def solve(html):
    seq = [c for c in html if c in ZW]
    top = [c for c, _ in Counter(seq).most_common(3)]
    for perm in itertools.permutations("STL"):
        m = dict(zip(top, perm))
        code = "".join(m[c] for c in seq if c in m)
        try:
            out = run(code)
        except Exception:
            continue
        if out.isprintable() and out:
            return out

if __name__ == "__main__":
    print(solve(fetch(sys.argv[1] if len(sys.argv) > 1 else "index.html")))
