import json
import re

import trainers_ordered_by_index as trainers_ordered_by_index

TRAINERS_FILE = "trainers.js"
SAVE_FILE = "save.json"


def get_trainer_splits_and_positions(content):
    """Parses trainers while keeping track of their exact char spans in content."""
    match = re.search(r"const TRAINERS = \[(.*?)\];", content, re.DOTALL)
    if not match:
        raise ValueError("Could not locate TRAINERS array in trainers.js")

    array_body = match.group(1)
    array_start_offset = match.start(1)

    trainer_pattern = re.compile(r'\{\s*n:\s*"(?P<n>.*?)"\s*,\s*s:\s*"(?P<s>.*?)"\s*\}')

    trainers = []
    for m in trainer_pattern.finditer(array_body):
        abs_start = array_start_offset + m.start()
        abs_end = array_start_offset + m.end()
        trainers.append(
            {
                "n": m.group("n"),
                "s": m.group("s"),
                "start": abs_start,
                "end": abs_end,
            }
        )

    return trainers


def update_trainers_and_save():
    with open(TRAINERS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    trainers = get_trainer_splits_and_positions(content)
    total_trainers = len(trainers)

    print(f"Current total trainers: {total_trainers}")

    try:
        target_idx = int(input("Where would you like to add a new trainer? "))
    except ValueError:
        print("Invalid number entered.")
        return

    if not (0 <= target_idx <= total_trainers):
        print(f"Index out of bounds (0 to {total_trainers}).")
        return

    trainer_name = input("Name of Trainer?\n").strip()
    if not trainer_name:
        print("Trainer name cannot be empty.")
        return

    # Determine split string dynamically
    prev_split = trainers[target_idx - 1]["s"] if target_idx > 0 else None
    next_split = trainers[target_idx]["s"] if target_idx < total_trainers else None

    if prev_split == next_split and prev_split is not None:
        assigned_split = prev_split
        print(f"Assigned split automatically: '{assigned_split}'")
    else:
        print("\nThe boundary indices have differing splits:")
        if prev_split:
            print(
                f"  [{target_idx - 1}]: {trainers[target_idx - 1]['n']} ({prev_split})"
            )
        if next_split:
            print(f"  [{target_idx}]: {trainers[target_idx]['n']} ({next_split})")

        choice = input(
            f"Which split should '{trainer_name}' belong to?\n"
            f"1) {prev_split}\n"
            f"2) {next_split}\n"
            "Choice (1/2): "
        ).strip()

        assigned_split = prev_split if choice == "1" else next_split

    new_entry_str = f'{{ n: "{trainer_name}", s: "{assigned_split}" }}'

    # 1. Update trainers.js by slicing the string around the target insertion point
    if target_idx < total_trainers:
        # Insert before the trainer currently at target_idx
        insert_pos = trainers[target_idx]["start"]
        updated_content = (
            content[:insert_pos] + new_entry_str + ",\n  " + content[insert_pos:]
        )
    else:
        # Append at the end of the array if target_idx is the very end
        insert_pos = trainers[-1]["end"]
        updated_content = (
            content[:insert_pos] + ",\n  " + new_entry_str + content[insert_pos:]
        )

    with open(TRAINERS_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(
        f"\nUpdated {TRAINERS_FILE} (inserted '{trainer_name}' at index {target_idx})."
    )

    # 2. Update save.json safely
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for attempt in data.get("attempts", []):
        deaths = attempt.get("deaths", [])

        if len(deaths) >= target_idx:
            deaths.insert(target_idx, 0)
        else:
            deaths.append(0)

        ended_at = attempt.get("endedAtIndex")
        current_at = attempt.get("currentIndex")

        if ended_at is not None and ended_at >= target_idx:
            attempt["endedAtIndex"] += 1

        if current_at is not None and current_at >= target_idx:
            attempt["currentIndex"] += 1

        if "skipped" in attempt and isinstance(attempt["skipped"], list):
            attempt["skipped"] = [
                idx + 1 if idx >= target_idx else idx for idx in attempt["skipped"]
            ]

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully updated all attempts in {SAVE_FILE}.")


if __name__ == "__main__":
    update_trainers_and_save()
    trainers_ordered_by_index.export_indexed_trainers()
