import os
import re
import sys

# https://matt.might.net/articles/shell-scripts-for-passive-voice-weasel-words-duplicates/

weasel_words = [
    "many",
    "various",
    "very",
    "fairly",
    "several",
    "extremely",
    "exceedingly",
    "quite",
    "remarkably",
    "few",
    "surprisingly",
    "mostly",
    "largely",
    "huge",
    "tiny",
    "((are|is) a number)",
    "excellent",
    "interestingly",
    "significantly",
    "substantially",
    "clearly",
    "vast",
    "relatively",
    "completely",
]

weasel_pattern = re.compile(rf"\b({"|".join(weasel_words)})\b", re.IGNORECASE)

irregular_words = [
    "awoken",
    "been",
    "born",
    "beat",
    "become",
    "begun",
    "bent",
    "beset",
    "bet",
    "bid",
    "bidden",
    "bound",
    "bitten",
    "bled",
    "blown",
    "broken",
    "bred",
    "brought",
    "broadcast",
    "built",
    "burnt",
    "burst",
    "bought",
    "cast",
    "caught",
    "chosen",
    "clung",
    "come",
    "cost",
    "crept",
    "cut",
    "dealt",
    "dug",
    "dived",
    "done",
    "drawn",
    "dreamt",
    "driven",
    "drunk",
    "eaten",
    "fallen",
    "fed",
    "felt",
    "fought",
    "found",
    "fit",
    "fled",
    "flung",
    "flown",
    "forbidden",
    "forgotten",
    "foregone",
    "forgiven",
    "forsaken",
    "frozen",
    "gotten",
    "given",
    "gone",
    "ground",
    "grown",
    "hung",
    "heard",
    "hidden",
    "hit",
    "held",
    "hurt",
    "kept",
    "knelt",
    "knit",
    "known",
    "laid",
    "led",
    "leapt",
    "learnt",
    "left",
    "lent",
    "let",
    "lain",
    "lighted",
    "lost",
    "made",
    "meant",
    "met",
    "misspelt",
    "mistaken",
    "mown",
    "overcome",
    "overdone",
    "overtaken",
    "overthrown",
    "paid",
    "pled",
    "proven",
    "put",
    "quit",
    "read",
    "rid",
    "ridden",
    "rung",
    "risen",
    "run",
    "sawn",
    "said",
    "seen",
    "sought",
    "sold",
    "sent",
    "set",
    "sewn",
    "shaken",
    "shaven",
    "shorn",
    "shed",
    "shone",
    "shod",
    "shot",
    "shown",
    "shrunk",
    "shut",
    "sung",
    "sunk",
    "sat",
    "slept",
    "slain",
    "slid",
    "slung",
    "slit",
    "smitten",
    "sown",
    "spoken",
    "sped",
    "spent",
    "spilt",
    "spun",
    "spit",
    "split",
    "spread",
    "sprung",
    "stood",
    "stolen",
    "stuck",
    "stung",
    "stunk",
    "stridden",
    "struck",
    "strung",
    "striven",
    "sworn",
    "swept",
    "swollen",
    "swum",
    "swung",
    "taken",
    "taught",
    "torn",
    "told",
    "thought",
    "thrived",
    "thrown",
    "thrust",
    "trodden",
    "understood",
    "upheld",
    "upset",
    "woken",
    "worn",
    "woven",
    "wed",
    "wept",
    "wound",
    "won",
    "withheld",
    "withstood",
    "wrung",
    "written",
]

irregular_pattern = re.compile(
    rf"\b(am|are|were|being|is|been|was|be)\b[ ]*(\w+ed|({"|".join(irregular_words)}))\b",
    re.IGNORECASE,
)


def find_duplicate_adjacent_words(filename):
    # Initialize the duplicate count
    dup_count = 0

    try:
        with open(filename, "r") as file:
            last_word = ""
            line_num = 0

            for line in file:
                line_num += 1
                # Split the line into words, keeping the delimiters
                words = re.split(r"(\W+)", line)

                for word in words:
                    # Skip spaces and empty words
                    if re.match(r"^\s*$", word):
                        continue

                    # Skip punctuation and reset last_word
                    if re.match(r"^\W+$", word):
                        last_word = ""
                        continue

                    # Check for duplicate adjacent words (case insensitive)
                    if word.lower() == last_word.lower():
                        print(f"{filename}:{line_num} {word.strip()}")
                        dup_count += 1

                    # Update last_word to the current word
                    last_word = word

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except IOError as e:
        print(f"Error reading file {filename}: {e}")

    return dup_count


if len(sys.argv) < 2:
    print(f"usage: {os.path.basename(sys.argv[0])} <file> ...")
    sys.exit(1)


for filename in sys.argv[1:]:
    try:
        with open(filename, "r") as f:
            for line_number, line in enumerate(f, start=1):
                if weasel_pattern.search(line):
                    highlighted_line = weasel_pattern.sub(r"\033[31m\1\033[0m", line)
                    print(f"{filename}:{line_number}:{highlighted_line.strip()}")
                elif irregular_pattern.search(line):
                    highlighted_line = irregular_pattern.sub(r"\033[31m\1\033[0m", line)
                    print(f"{filename}:{line_number}:{highlighted_line.strip()}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

    find_duplicate_adjacent_words(filename)
