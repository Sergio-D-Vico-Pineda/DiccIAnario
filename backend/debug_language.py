from app.utils.language_detector import is_spanish, _detector, _has_lib


def dump(term: str) -> None:
    print('term', term)
    print('is_spanish', is_spanish(term))
    if _has_lib and _detector is not None:
        values = _detector.compute_language_confidence_values(term)
        for item in values:
            print(getattr(item, 'language', None), float(getattr(item, 'value', 0.0)))


if __name__ == '__main__':
    print('has_lib', _has_lib)
    for term in ['hecatombe', 'válido', 'running', 'gato']:
        dump(term)
        print('---')
