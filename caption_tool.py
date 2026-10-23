
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


def to_srt_time(milliseconds):
    """Convert milliseconds to SRT timestamp format."""
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    seconds = (milliseconds % 60_000) // 1_000
    millis = milliseconds % 1_000

    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def export_srt(lines, filename="captions.srt", seconds_per_line=2):
    """Export captions with simple estimated timing."""
    with open(filename, "w", encoding="utf-8") as file:
        for index, line in enumerate(lines):
            start = index * seconds_per_line * 1000
            end = start + seconds_per_line * 1000

            file.write(f"{index + 1}\n")
            file.write(
                f"{to_srt_time(start)} --> {to_srt_time(end)}\n"
            )
            file.write(f"{line}\n\n")


if __name__ == "__main__":
    text = input("Paste your reel script: ")

    try:
        max_chars = int(input("Max characters per line (32): ") or 32)
        seconds = float(input("Seconds per caption (2): ") or 2)

        if max_chars < 1 or seconds <= 0:
            raise ValueError

    except ValueError:
        print("Enter a positive character limit and duration.")
    else:
        captions = split_captions(text, max_chars)
        export_srt(captions, seconds_per_line=seconds)

        print(f"\nCreated captions.srt with {len(captions)} captions.")
        print("Import captions.srt into Premiere Pro to review.")
