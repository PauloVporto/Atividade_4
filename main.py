import json

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory # convert select queries results in dict


cloud_config= {
  "secure_connect_bundle": "secure-connect.zip"
}


with open("s202-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
cassandra_session = cluster.connect()
cassandra_session.row_factory = dict_factory

# Use your keyspace name
cassandra_session.set_keyspace("montadora")

# Questão 1

cassandra_session.execute("DROP TABLE IF EXISTS estoque;")
query = ''' 
    CREATE TABLE estoque(
        id int, 
        nome text, 
        carro text, 
        estante int, 
        nivel int,
        quantidade int,
        primary key((carro), estante, nivel, id)
    );
'''
cassandra_session.execute(query)
cassandra_session.execute("TRUNCATE estoque;")


query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (5, "Pistão", "Mustang", 4, 1, 167))

query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (4, "Suspensão", "Argo", 1, 1, 3500))

### Extras

query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (4, "Pistão", "Argo", 1, 2, 1500))
query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (4, "Suspensão", "Mustang", 3, 5, 200))
query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (4, "Correia", "Argo", 1, 3, 2540))
query = """ INSERT INTO estoque(id, nome, carro, estante, nivel, quantidade) VALUES (%s, %s, %s, %s, %s, %s) """
cassandra_session.execute(query, (4, "Cabo Câmbio", "Argo", 1, 5, 1560))


# Questão 2
# a)
query = """ SELECT * FROM estoque WHERE nome = 'Pistão' ALLOW FILTERING; """
result = cassandra_session.execute(query).all()

print("Dados das peças com nome de 'Pistão': ")
if result is not None:
  for r in result:
    print(r)

# b)
query = """ SELECT AVG(quantidade) FROM estoque; """
result = cassandra_session.execute(query).one()

print("Média das quantidadea das peças em estoque: ")
print(result)

# c)
query = """ SELECT COUNT(*) FROM estoque; """
result = cassandra_session.execute(query).one()

print("Quantidade de registros na tabela 'estoque': ")
print(result)

# d)
query = """ SELECT MAX(quantidade) AS maior_quantidade, MIN(quantidade) AS menor_quantidade FROM estoque; """
result = cassandra_session.execute(query).one()

print("Maior e menor quantidade de peças no estoque: ")
print(result)

# e)
query = """ SELECT nome, carro, quantidade FROM estoque WHERE estante = 3 ALLOW FILTERING; """
result = cassandra_session.execute(query).all()

print("Informações sobre as peças na estante 3: ")
if result is not None:
  for r in result:
    print(r)

# f)
query = """ SELECT AVG(quantidade) FROM estoque WHERE nivel = 1 ALLOW FILTERING; """
result = cassandra_session.execute(query).one()

print("Média da quantidade de peças no nível 1: ")
print(result)

# g)
query = """ SELECT * FROM estoque WHERE estante < 3 AND nivel > 4  ALLOW FILTERING; """
result = cassandra_session.execute(query).all()

print("Peças nas estahntes com núemro menor que 3 e nível maior que 4: ")
if result is not None:
  for r in result:
    print(r)


# Questão 3
while(True):
    try:
        carro = str(input("Entre com o nome do carro para recuperar as informações sobre suas peças (Ctrl+C para sair): "))

        result = cassandra_session.execute(f"SELECT nome, estante, quantidade FROM estoque WHERE carro = '{carro}' ALLOW FILTERING;").all()

        if result is not None:
            for r in result:
                print(r)
    except:
       print("Saindo...")
       break