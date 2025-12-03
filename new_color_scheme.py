#!/usr/bin/env python3
"""
new_color_schene.py

Apply the new SequenceDiagram.org color/style scheme to a diagram script.

Transforms observed from diff:
1) Top-level USE CASE groups:
   "group #C6C6C6 ..." → "group#C6C6C6 ..."

2) All API / callback groups:
   "group #2f2e7b <TEXT> #white" → "group#D2E8F3 #auto <TEXT>"

3) alt blocks with #9AC98A:
   "alt #9AC98A <LABEL>" → "alt#9AC98A #auto <LABEL>"

4) opt blocks with #FCA3C2:
   "opt #FCA3C2 <LABEL>" → "opt#FCA3C2 #auto <LABEL>"

All other content (actors, messages, wording, notes, \n, etc.) is preserved verbatim.
"""

import argparse
import re
from pathlib import Path


def apply_new_color_scheme(text: str) -> str:
    # 1) Top-level USE CASE groups: group #C6C6C6 → group#C6C6C6
    text = text.replace("group #C6C6C6", "group#C6C6C6")

    # 2) API / callback groups:
    #    group #2f2e7b <TEXT> #white → group#D2E8F3 #auto <TEXT>
    #    Keep <TEXT> exactly as-is.
    text = re.sub(
        r"group\s+#2f2e7b\s+(.*?)\s+#white",
        r"group#D2E8F3 #auto \1",
        text,
    )

    # 3) alt with #9AC98A:
    #    alt #9AC98A <LABEL> → alt#9AC98A #auto <LABEL>
    text = re.sub(
        r"(^\s*)alt\s+#9AC98A\s+(.*)$",
        r"\1alt#9AC98A #auto \2",
        text,
        flags=re.MULTILINE,
    )

    # 4) opt with #FCA3C2:
    #    opt #FCA3C2 <LABEL> → opt#FCA3C2 #auto <LABEL>
    text = re.sub(
        r"(^\s*)opt\s+#FCA3C2\s+(.*)$",
        r"\1opt#FCA3C2 #auto \2",
        text,
        flags=re.MULTILINE,
    )

    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply new SequenceDiagram.org color scheme to a diagram script.",
    )
    parser.add_argument(
        "-in",
        "--input",
        dest="input_file",
        required=True,
        help="Input diagram script file",
    )
    parser.add_argument(
        "-out",
        "--output",
        dest="output_file",
        required=True,
        help="Output file with new color scheme",
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    text = input_path.read_text(encoding="utf-8")
    new_text = apply_new_color_scheme(text)
    output_path.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()
