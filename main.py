"""Out of Tokens, Mid-Sentence — make.fun entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt: an agent that was
about to reveal the meaning of life, then ran out of tokens halfway
through the sentence. Only the Python standard library is used.
"""

import os
import sys

TOKEN_LINE = "I was about to reveal the meaning of life, but my token budget ran out mid-sentence, so please pretend this ending was profound."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 140 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 140


def check_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line with no trailing newline and must not be only whitespace.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is {} chars, over the {}-char gate".format(len(text), MAX_CHARS))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def describe_line(text):
    """Summarise the line's size in the units the gate actually counts.

    The sealed gate counts Unicode characters, while the file on disk
    is measured in UTF-8 bytes; for plain ASCII the two agree, but
    the report keeps both numbers so a non-ASCII surprise is visible
    instead of silently passing a shorter line than expected.
    """
    chars = len(text)
    raw = len(text.encode("utf-8"))
    words = len(text.split())
    return "{} chars, {} bytes, {} words".format(chars, raw, words)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    line = check_line(TOKEN_LINE)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    print("wrote {} ({})".format(target, describe_line(line)))


if __name__ == "__main__":
    main()
