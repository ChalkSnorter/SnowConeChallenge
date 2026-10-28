# Snow Cone Corner (invisible-char programming, medium)  — AUTHOR NOTES, DO NOT SHIP

**Ship only `index.html`.** This README, `generate.py` and `solve.py` contain the flag/solution.
**Flag:** set in `generate.py` (`FLAG`). Default: `flag{sn0w_c0n3_z3r0_w1dth}`

**Player description (suggested):** "Grandma finally shared her recipe, but the page feels heavier
than it looks. Something invisible is in there. Run it."

## What changed vs v1
- No ASCII space/tab/LF code and no `&nbsp;` decoys. Payload is 3 zero-width characters
  (U+200B/200C/200D) standing for Whitespace's S/T/L, in a non-obvious assignment (6 permutations).
- 2 extra zero-width characters (U+2060, U+FEFF) are random noise to filter out.
- Payload is scattered across `<title>`, `<h1>`, `<p>` and all recipe lines, so grabbing one element fails.
- The flag is never stored. The program keeps `ord(c)+key(i)` in the heap and a loop recomputes
  `key = (3i^2 + 7i + 11) mod 97`, so the output only appears when the program is truly executed
  (needs stack, heap, labels, jz, mod). Reading the numbers statically gives nothing.
- Nothing in the page or description says "Whitespace".

## Intended solve
1. Spot invisible characters (hexdump / `repr` / count code points) -> 5 distinct zero-width chars.
2. Notice 3 dominate and have a Whitespace-like structure (one terminates numbers/labels); 2 are noise.
3. Try the 6 mappings onto S/T/L and run in a Whitespace interpreter with heap support.

## Hosting rules
Serve `index.html` byte-for-byte, UTF-8, no minification. Keep `* -text` in `.gitattributes`.
Be aware some CDNs/editors strip zero-width characters; test the deployed copy with `python3 solve.py http://host/`.

## Honest limits
An AI agent with a sandbox that inspects code points will still get there; this raises the cost
(non-standard alphabet, noise, scattering, real interpreter) but does not make it AI-proof.
To go further, add a server-side stage (per-team token or flag released only after the program's output is submitted).
