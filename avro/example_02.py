from avro_helper import avro_object_to_bin, avro_bin_to_object

# Definindo um schema
schema = {
    "name": "Parent",
    "type": "record",
    "fields": [
        {
            "name": "children",
            "type": {
                "type": "array",
                "items": {
                    "name": "Child",
                    "type": "record",
                    "fields": [
                        {"name": "name", "type": "string"}
                    ]
                }
            }
        }
    ]
}


# Definindo um objeto referente ao schema
objeto = {
    "children": [
        {"name": "Guionardo"},
        {"name": "Otávio"}
    ]
}
print('Objeto original', objeto, '\n')
# Objeto original {'id': 1, 'nome': 'Guionardo', 'empresa': {'id': 5, 'nome': 'HBSIS'}}

# Convertendo o objeto para um binário avro
# schema pode ser um dict, como no exemplo, mas também pode ser um string JSON, um nome de arquivo ou uma URL com conteúdo JSON
ret = avro_object_to_bin(objeto, schema)
# O retorno da função é uma tupla, onde o primeiro elemento é boolean representando o sucesso.
# O segundo elemento é o conteúdo ou uma mensagem de erro, dependendo do sucesso
# O terceiro elemento mostra as informações do schema utilizado

print('Retorno da conversão:', ret)
# Retorno da conversão: (True, b'Obj\x01\x04\x14avro.codec\x08null\x16avro.schema\x92\x05{"type": "record", "name": "Usuario", "namespace": "teste", "fields": [{"type": "int", "name": "id"}, {"type": "string", "name": "nome"}, {"namespace": "teste", "type": {"type": "record", "name": "empresa", "namespace": "teste", "fields": [{"type": "int", "name": "id"}, {"type": "string", "name": "nome"}]}, "name": "empresa"}]}\x00\xe4k\xe6O\x8c\x1b\x93\x1b\x1f+\x90UH\xa3\x0b\xb7\x02$\x02\x12Guionardo\n\nHBSIS\xe4k\xe6O\x8c\x1b\x93\x1b\x1f+\x90UH\xa3\x0b\xb7')

# Simulando um erro de schema, alterei o type do id de 'int' para 'into'
# Retorno da conversão: (False, "Unknown named schema 'into', known names: ['teste.Usuario', 'teste.empresa'].")


if (ret[0]):
    print('\nConversão com sucesso')
    ret = avro_bin_to_object(ret[1])
    print('Objeto recuperado:', ret[1])
    # Objeto recuperado: (True, [{'id': 1, 'nome': 'Guionardo', 'empresa': {'id': 5, 'nome': 'HBSIS'}}])
    print('Schema:', ret[2])
    # Schema: {'namespace': 'teste', 'type': 'record', 'name': 'Usuario', 'origin': ('binary', None)}
else:
    print('Conversão com erro:', ret[1])
    # Conversão com erro: Unknown named schema 'into', known names: ['teste.Usuario', 'teste.empresa'].
