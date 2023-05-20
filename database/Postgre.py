from peewee import Model, CharField, PostgresqlDatabase

# conexão com o banco
db = PostgresqlDatabase('tcc_database', user='marcos', password='marcos', host='localhost', port=5432)


class Cidades(Model):
    cidade = CharField()
    estado = CharField()

    class Meta:
        database = db

    @staticmethod
    def init():
        db.drop_tables([Cidades])
        db.create_tables([Cidades])


