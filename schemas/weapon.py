import whoosh.fields

from schemas.schema import _Schema


class Weapon(_Schema):

    profile_type = 'Weapon'

    whoosh_schema = whoosh.fields.Schema(
        document_type=whoosh.fields.ID(stored=True),
        faction=whoosh.fields.ID(stored=True),
        name=whoosh.fields.NGRAM(stored=True),
        book=whoosh.fields.ID(stored=True),
        page=whoosh.fields.ID(stored=True),
        type=whoosh.fields.ID(stored=True),
        range=whoosh.fields.ID(stored=True),
        s=whoosh.fields.ID(stored=True),
        ap=whoosh.fields.ID(stored=True),
        d=whoosh.fields.ID(stored=True),
        abilities=whoosh.fields.ID(stored=True)
    )

    @staticmethod
    def write_document(writer, profile):
        writer.add_document(
            document_type='weapon',
            faction=profile.get('faction'),
            name=profile.get('name'),
            book=profile.get('book'),
            page=profile.get('page'),
            type=profile.get('Type'),
            range=profile.get('Range'),
            s=profile.get('S'),
            ap=profile.get('AP'),
            d=profile.get('D'),
            abilities=profile.get('Abilities')
        )
