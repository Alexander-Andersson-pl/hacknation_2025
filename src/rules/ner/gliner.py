# src/rules/ner/gliner_rule.py

from functools import lru_cache
from typing import List, Dict

from gliner import GLiNER


MODEL_NAME = "urchade/gliner_multi-v2.1"  # multilingual, sensowne na PL


@lru_cache(maxsize=1)
def get_model() -> GLiNER:
    """
    Lazy load – model ładuje się tylko przy pierwszym wywołaniu.
    """
    return GLiNER.from_pretrained(MODEL_NAME, load_tokenizer=True)


_GL_LABELS = [
    "religious affiliation",
    "religious belief",
    "political ideology",
    "political party",
    "health condition",
    "medical condition",
    "sexual orientation",
    "ethnic group",
]

_LABEL_TO_PLACEHOLDER: Dict[str, str] = {
    "religious affiliation": "[religion]",
    "religious belief": "[religion]",
    "political ideology": "[political_view]",
    "political party": "[political_view]",
    "health condition": "[health]",
    "medical condition": "[health]",
    "sexual orientation": "[sexual_orientation]",
    "ethnic group": "[ethnicity]",
}

_LABEL_TO_PLACEHOLDER = {k.lower(): v for k, v in _LABEL_TO_PLACEHOLDER.items()}
model = get_model()

class GlinerSensitive:
    @staticmethod
    def anonymize(text: str, threshold: float = 0.5) -> str:
        model = get_model()

        entities: List[dict] = model.predict_entities(
            text,
            labels=_GL_LABELS,
            threshold=threshold,
        )

        for ent in sorted(entities, key=lambda e: e["start"], reverse=True):
            label_key = ent["label"].lower()
            placeholder = _LABEL_TO_PLACEHOLDER.get(label_key)
            if not placeholder:
                continue

            start, end = ent["start"], ent["end"]
            text = text[:start] + placeholder + text[end:]

        return text
