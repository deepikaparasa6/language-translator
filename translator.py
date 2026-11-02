"""
translator.py
-------------
Core translation logic and language management module.
Uses GoogleTranslator from deep-translator with reliable API fallback.
"""

import requests
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

# Curated fallback language list in case network is unreachable on startup
FALLBACK_LANGUAGES = [
    "english", "hindi", "spanish", "french", "german",
    "bengali", "marathi", "telugu", "tamil", "gujarati",
    "urdu", "russian", "japanese", "korean", "chinese (simplified)",
    "arabic", "portuguese", "italian"
]


def get_available_languages():
    """
    Fetch the list of supported languages dynamically from GoogleTranslator.
    If the network request fails, fall back to the known dictionary of languages.
    Returns a sorted list of human-readable, title-cased language names.
    """
    try:
        # Dynamically retrieve supported languages from GoogleTranslator
        languages = GoogleTranslator().get_supported_languages()
        if not languages:
            languages = list(GOOGLE_LANGUAGES_TO_CODES.keys())
    except Exception:
        # Fallback if offline or service is unreachable
        languages = list(GOOGLE_LANGUAGES_TO_CODES.keys()) if GOOGLE_LANGUAGES_TO_CODES else FALLBACK_LANGUAGES

    # Format languages to Title Case for a clean, user-friendly UI display
    formatted_languages = sorted([lang.title() for lang in languages])
    return formatted_languages


def _resolve_lang_code(lang_name: str) -> str:
    """
    Helper function to convert a human-readable language name
    into its corresponding language code for Google Translate.
    """
    if not lang_name:
        return ""
    clean = lang_name.strip().lower()
    if clean in ["auto detect", "auto"]:
        return "auto"
    # Check if already a code (e.g. 'en', 'hi')
    if clean in GOOGLE_LANGUAGES_TO_CODES.values():
        return clean
    # Map from language name to code (e.g. 'hindi' -> 'hi')
    return GOOGLE_LANGUAGES_TO_CODES.get(clean, clean)


def _translate_via_api(text: str, source_code: str, target_code: str) -> str:
    """
    Direct Google Translate service call.
    Acts as a resilient fallback if deep-translator's default scraping endpoint
    encounters rate limits (HTTP 429).
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_code,
        "tl": target_code,
        "dt": "t",
        "q": text,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data and data[0]:
        translated_chunks = [part[0] for part in data[0] if part and part[0]]
        return "".join(translated_chunks)
    raise ValueError("Empty response received from translation service.")


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates input text from source_lang to target_lang.
    Handles input validation, 'Auto Detect', identical languages, and connection errors.
    """
    # 1. Validation: check for empty or whitespace-only input
    if not text or not text.strip():
        return "Please enter some text to translate."

    cleaned_text = text.strip()

    # 2. Normalize source and target language names
    if not source_lang or source_lang.strip().lower() in ["auto detect", "auto"]:
        src_name = "auto"
    else:
        src_name = source_lang.strip().lower()

    if not target_lang:
        return "Please select a target language."

    tgt_name = target_lang.strip().lower()

    # 3. Check if source and target languages are identical
    if src_name != "auto" and src_name == tgt_name:
        return f"Note: Source and target languages are identical.\n\n{cleaned_text}"

    # 4. Resolve language codes
    src_code = _resolve_lang_code(src_name)
    tgt_code = _resolve_lang_code(tgt_name)

    # Check if target language code resolved properly
    if not tgt_code:
        return "Invalid target language selected. Please choose a valid language."

    # 5. Perform translation using GoogleTranslator
    try:
        # First attempt: standard deep-translator GoogleTranslator
        translator = GoogleTranslator(source=src_name, target=tgt_name)
        translated = translator.translate(cleaned_text)

        if translated:
            return translated

        # If empty response, attempt direct service
        return _translate_via_api(cleaned_text, src_code, tgt_code)

    except Exception:
        # Second attempt: direct Google Translate API endpoint fallback
        try:
            return _translate_via_api(cleaned_text, src_code, tgt_code)
        except Exception:
            # User-friendly error message without exposing Python tracebacks
            return "Translation could not be completed. Please check your internet connection and try again."
