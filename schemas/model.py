import whoosh.fields

from schemas.schema import _Schema


class Model(_Schema):

    profile_type = 'Model'

    whoosh_schema = whoosh.fields.Schema(
        document_type=whoosh.fields.ID(stored=True),
        faction=whoosh.fields.ID(stored=True),
        name=whoosh.fields.NGRAM(stored=True)
    )

    @staticmethod
    def write_document(writer, profile):
        writer.add_document(
            document_type='weapon',
            faction=profile.get('faction'),
            name=profile.get('name')
        )
