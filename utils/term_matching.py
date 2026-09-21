"""Match whole skills without treating JavaScript as Java or C++ as C."""

import re


def contains_term(text: str, term: str) -> bool:
    """Match a case-insensitive term, allowing flexible phrase whitespace.

    Plus and hash are part of language names; a slash or hyphen may separate
    skills (for example Python/SQL or Java-based).
    """
    parts = term.strip().split()
    if not parts:
        return False
    pattern = r"(?<![\w+#])" + r"\s+".join(map(re.escape, parts)) + r"(?![\w+#])"
    return re.search(pattern, text, re.IGNORECASE) is not None
