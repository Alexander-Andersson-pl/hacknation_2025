import re
import spacy

# Load Polish model
nlp = spacy.load("pl_core_news_lg")

# Regex patterns for sensitive data
patterns = {
    "[phone]": r"\b(\+?48)?\s?(\d{3}[-\s]?){2}\d{3}\b",
    "[email]": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "[pesel]": r"\b\d{11}\b",
    "[nip]": r"\b\d{10}\b",
    "[regon]": r"\b\d{9}\b",
    "[postal_code]": r"\b\d{2}-\d{3}\b"
}

# Map spaCy NER labels → tokens
ner_map = {
    "PERSON": "[person]",
    "LOC": "[location]",
    "GPE": "[place]",
    "ORG": "[organization]"
}

def anonymize_text(text):
    doc = nlp(text)

    # 1. Apply regex-based masking
    for token, pattern in patterns.items():
        text = re.sub(pattern, token, text)

    # 2. Apply spaCy NER-based masking
    for ent in doc.ents:
        if ent.label_ in ner_map:
            token = ner_map[ent.label_]
            text = text.replace(ent.text, token)

    # 3. Rule-based context anonymization
    # Address detection ("ul. Grunwaldzka 12")
    text = re.sub(r"(ul\.?|ulica)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(\s+\d+[A-Za-z]?)?",
                  "[address]", text)

    return text


# 🔥 Example
text = """
Nazywam się Jan Kowalski, mój PESEL to 90010112345. Mieszkam w Warszawie przy ulicy Długiej 5.
"""

print(anonymize_text(text))