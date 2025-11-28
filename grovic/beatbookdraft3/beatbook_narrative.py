import re

def bullets_to_sentences(text: str) -> str:
    """
    Convert markdown bullet points (-, *, •) into narrative sentences.
    Keeps section headers, merges bullet points into flowing text.
    """

    lines = text.split("\n")
    new_lines = []
    buffer_sentences = []

    bullet_pattern = r"^\s*[\-\*\•]\s+"

    for line in lines:
        # If it's a header, flush the buffer and keep header
        if line.strip().startswith("#"):
            if buffer_sentences:
                new_lines.append(" ".join(buffer_sentences))
                buffer_sentences = []
            new_lines.append(line)
            continue

        # If it's a bullet, convert to sentence
        if re.match(bullet_pattern, line):
            cleaned = re.sub(bullet_pattern, "", line).strip()
            # Capitalize first letter
            cleaned = cleaned[0].upper() + cleaned[1:]
            # Add period if missing
            if cleaned and cleaned[-1] not in ".!?":
                cleaned += "."
            buffer_sentences.append(cleaned)
            continue

        # Normal line → flush bullet buffer and keep line
        if buffer_sentences:
            new_lines.append(" ".join(buffer_sentences))
            buffer_sentences = []

        new_lines.append(line)

    # Flush remaining buffer
    if buffer_sentences:
        new_lines.append(" ".join(buffer_sentences))

    return "\n".join(new_lines)


def convert_to_narrative(input_file="beatbook_combined.md",
                         output_file="beatbook_narrative.md"):

    with open(input_file, "r", encoding="utf-8") as f:
        original = f.read()

    narrative = bullets_to_sentences(original)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(narrative)

    print(f"✔ Narrative beatbook created: {output_file}")


if __name__ == "__main__":
    convert_to_narrative()
