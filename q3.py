from cassandra.cluster import Cluster

def consultar_estoque_por_carro(carro):
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('Auto')

    query = f"SELECT nome, estante, quantidade FROM estoque WHERE ocarro = '{carro}'"
    rows = session.execute(query)

    for row in rows:
        print(f"Nome: {row.nome}, Estante: {row.estante}, Quantidade: {row.quantidade}")

    cluster.shutdown()

carro_fornecido = input("Digite o nome do carro para consultar o estoque: ")
consultar_estoque_por_carro(carro_fornecido)