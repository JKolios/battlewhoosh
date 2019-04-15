import whoosh.fields


class Schema(whoosh.fields.SchemaClass):

    document_type = whoosh.fields.ID(stored=True)
    faction = whoosh.fields.ID(stored=True)
    name = whoosh.fields.NGRAM(stored=True, phrase=False)
    book = whoosh.fields.ID(stored=True)
    page = whoosh.fields.ID(stored=True)
    Type = whoosh.fields.ID(stored=True)
    Range = whoosh.fields.ID(stored=True)
    S = whoosh.fields.ID(stored=True)
    D = whoosh.fields.ID(stored=True)
    Abilities = whoosh.fields.ID(stored=True)
    AP = whoosh.fields.ID(stored=True)
    A = whoosh.fields.ID(stored=True)
    BS = whoosh.fields.ID(stored=True)
    WS = whoosh.fields.ID(stored=True)
    Ld = whoosh.fields.ID(stored=True)
    M = whoosh.fields.ID(stored=True)
    Max = whoosh.fields.ID(stored=True)
    S = whoosh.fields.ID(stored=True)
    T = whoosh.fields.ID(stored=True)
    Sv = whoosh.fields.ID(stored=True)
    W = whoosh.fields.ID(stored=True)
    Description = whoosh.fields.ID(stored=True)
    PsychicPower = whoosh.fields.ID(stored=True)
    Ability = whoosh.fields.ID(stored=True)
