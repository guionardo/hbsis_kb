# Testes de (de)serialização com AVRO

## Documentação

[Documentoação oficial](https://avro.apache.org/docs/current/index.html)

Avro é um sistema de serialização de dados, provendo estruturas de dados ricas, um formato de dados binário, compacto e rápido.

### Schemas

Avro depende de *schemas*. Quando dados Avro são lidos, o *schema* utilizado na escrita está sempre presente. Isso permite que cada dado seja escrito sem *overheads* por valor, fazendo com que a serialização seja rápida e pequena. Isso também facilita o uso de linguagens scripts dinâmicas, já que os dados, com seu *schema*, são completamente auto-descritivos.

## Utilização

### Python

Durante a escrita desta documentação, foram utilizados os seguintes pacotes disponíveis pelo [PyPI](https://pypi.org) e instaláveis pelo comando abaixo:

``` bash
pip install avro-json-serializer avro-python3
```