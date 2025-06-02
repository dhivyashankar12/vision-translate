from langdetect import detect
from googletrans import Translator

# A dictionary of supported languages (Google Translate format)
languages = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'ar': 'Arabic',
    # Add more if needed
}

translator = Translator()

def detect_language(text):
    """
    Detects the language of the input text.
    Returns: (language_code, language_name)
    """
    try:
        lang_code = detect(text)
        lang_name = languages.get(lang_code, "Unknown")
        return lang_code, lang_name
    except Exception as e:
        return "en", "English"  # Default fallback

def translate_text(text, target_lang):
    """
    Translates text to the target language.
    Returns: Translated text
    """
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return "Translation failed. Please try again."
