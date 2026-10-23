import re


def split_captions(text, max_chars=32):
    """Split text into readable caption lines."""
    words = re.findall(r"\S+", text.strip())
    lines = []
    current = ""

    for word in words:
        if len(word) > max_chars:
            if current:
                lines.append(current)
                current = ""
            lines.append(word)
            continue

        candidate = f"{current} {word}".strip()

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


if __name__ == "__main__":
    sample = input("Enter your reel caption text: ")
    try:
        limit = int(input("Maximum characters per line (default 32): ") or 32)
        if limit < 1:
            raise ValueError
    except ValueError:
        print("Please enter a positive whole number.")
    else:
        print("\n--- Caption Lines ---")
        for index, line in enumerate(split_captions(sample, limit), 1):
            print(f"{index:02d}: {line}")
