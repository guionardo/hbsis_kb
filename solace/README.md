# SETUP Solace

Repositório original [aqui](https://github.com/SolaceLabs/solace-single-docker-compose)

Informações [complementares](README_EN.md)

Arquivo yml do docker-compose foi alterado em relação ao original, abrindo as portas de conexão MQTT

Execute o seguinte comando para criar o message broker PubSub+ com o arquivo [PubSubStandard_singleNode.yml](template/PubSubStandard_singleNode.yml)

``` bash
docker-compose -f PubSubStandard_singleNode.yml up -d
```

Foram feitos testes de conexão utilizando os clientes abaixo:

* [ ] Solace Clients: Não foi possível executar com os fontes python informados.
* [X] MQTT: Operação normal, com POST e SUBSCRIBE
* [ ] REST: POST foi possível, mas não foi possível fazer o SUBSCRIBE e obter as informações da fila
* [ ] AMQP: Não testado

## Informações específicas e documentação

* https://solace.com/samples/solace-samples-rest-messaging/publish-subscribe/

* <https://github.com/SolaceSamples/solace-samples-amqp-qpid-proton-python>