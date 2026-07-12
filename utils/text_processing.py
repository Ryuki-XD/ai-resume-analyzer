"""Text processing utilities for NLP operations.

Provides functions for text cleaning, tokenization, and keyword
extraction using NLTK and scikit-learn's TF-IDF vectorizer.
"""

from __future__ import annotations

import re

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# NLTK bootstrap — download required data on first import
# ---------------------------------------------------------------------------
_NLTK_PACKAGES = ["punkt_tab", "stopwords"]

for _pkg in _NLTK_PACKAGES:
    try:
        nltk.data.find(f"tokenizers/{_pkg}" if "punkt" in _pkg else f"corpora/{_pkg}")
    except LookupError:
        logger.info("Downloading NLTK package: %s", _pkg)
        nltk.download(_pkg, quiet=True)

from nltk.corpus import stopwords  # noqa: E402
from nltk.tokenize import word_tokenize  # noqa: E402

_STOP_WORDS: set[str] = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """Normalize text for analysis.

    Lowercases, removes non-alphanumeric characters (keeping spaces),
    and collapses multiple whitespace into single spaces.

    Args:
        text: Raw input text.

    Returns:
        Cleaned text string.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s.#+/\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """Tokenize text into individual words.

    Args:
        text: Input text (ideally already cleaned).
        remove_stopwords: Whether to filter out English stopwords.

    Returns:
        List of tokens.
    """
    tokens = word_tokenize(clean_text(text))
    if remove_stopwords:
        tokens = [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]
    return tokens


def extract_keywords(
    text: str,
    top_n: int = 30,
    ngram_range: tuple[int, int] = (1, 2),
) -> list[str]:
    """Extract the most important keywords from text using TF-IDF.

    Uses a single-document TF-IDF approach — term frequency acts as the
    primary signal since IDF is uniform for a single document.

    Args:
        text: Input text to extract keywords from.
        top_n: Number of top keywords to return.
        ngram_range: Min and max n-gram sizes to consider.

    Returns:
        List of keywords sorted by TF-IDF score (descending).
    """
    cleaned = clean_text(text)
    if not cleaned.strip():
        return []

    vectorizer = TfidfVectorizer(
        max_features=200,
        stop_words="english",
        ngram_range=ngram_range,
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([cleaned])
    except ValueError:
        logger.warning("TF-IDF extraction failed — text may be too short.")
        return []

    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray().flatten()

    # Sort features by score in descending order
    ranked_indices = scores.argsort()[::-1][:top_n]
    keywords = [feature_names[i] for i in ranked_indices if scores[i] > 0]

    logger.debug("Extracted %d keywords from text.", len(keywords))
    return keywords


def compute_cosine_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using TF-IDF.

    Args:
        text_a: First text document.
        text_b: Second text document.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    from sklearn.metrics.pairwise import cosine_similarity

    cleaned_a = clean_text(text_a)
    cleaned_b = clean_text(text_b)

    if not cleaned_a.strip() or not cleaned_b.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        tfidf_matrix = vectorizer.fit_transform([cleaned_a, cleaned_b])
    except ValueError:
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity[0][0])
