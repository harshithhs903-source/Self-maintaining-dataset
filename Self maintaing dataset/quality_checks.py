def is_too_short(text, min_words=6):
    return len(text.split()) < min_words


def is_duplicate(text, existing_texts):
    return text in existing_texts


def quality_check(text, existing_texts):
    if is_too_short(text):
        return "DROP_SHORT"
    if is_duplicate(text, existing_texts):
        return "DROP_DUPLICATE"
    return "KEEP"