def my_split(text, delimiter=" "):
    parts = []
    current = ""
    for char in text:
        if char == delimiter:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts