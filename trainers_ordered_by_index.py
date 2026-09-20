import re

TRAINERS_FILE = "trainers.js"
OUTPUT_FILE = "trainers_list.txt"


def export_indexed_trainers():
    try:
        with open(TRAINERS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{TRAINERS_FILE}'.")
        return

    # Extract the JS array contents
    match = re.search(r"const TRAINERS = \[(.*?)\];", content, re.DOTALL)
    if not match:
        print("Error: Could not parse TRAINERS array structure.")
        return

    array_body = match.group(1)

    # Match individual trainer entries: { n: "Name", s: "Split" }
    trainer_pattern = re.compile(r'\{\s*n:\s*"(?P<n>.*?)"\s*,\s*s:\s*"(?P<s>.*?)"\s*\}')
    trainers = trainer_pattern.findall(array_body)

    if not trainers:
        print("No trainers found in the array.")
        return

    # Calculate padding width based on total count for neat alignment
    pad_width = len(str(len(trainers) - 1))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Total Trainers: {len(trainers)}\n")
        f.write("=" * 40 + "\n\n")

        for idx, (name, split) in enumerate(trainers):
            f.write(f"[{idx:>{pad_width}}] {name} ({split})\n")

    print(f"Successfully exported {len(trainers)} trainers to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    export_indexed_trainers()
