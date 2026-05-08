POS_MAP = {
    "VERB": "verbo",
    "AUX": "verbo",
    "NOUN": "sustantivo",
    "PROPN": "sustantivo propio",
    "ADJ": "adjetivo",
    "ADV": "adverbio",
    "DET": "determinante",
    "PRON": "pronombre",
    "ADP": "preposición",
    "CCONJ": "conjunción",
    "SCONJ": "conjunción",
    "INTJ": "interjección",
}


def map_pos_to_classification(pos: str) -> str:
    return POS_MAP.get(pos, "desconocida")