from whoosh.fields import Schema, TEXT, ID, NGRAM
from whoosh.analysis import StemmingAnalyzer

weapon = Schema(
    document_type=ID(stored=True),
    faction=ID(stored=True),
    name=NGRAM(stored=True),
    book=ID(stored=True),
    page=ID(stored=True),
    type=ID(stored=True),
    range=ID(stored=True),
    s=ID(stored=True),
    ap=ID(stored=True),
    d=ID(stored=True),
    abilities=ID(stored=True)
)