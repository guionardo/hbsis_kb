# Desenvolvimento de uma classe Python para comunicação com o SOLACE via REST

https://solace.com/samples/solace-samples-rest-messaging/publish-subscribe/
https://solace.com/samples/solace-samples-mqtt/


Comando para teste

```
curl -X POST -d "Hello World REST 2" http://localhost:9000/T/rest/pubsub -H "content-type: text" -H "Solace-delivery-mode: persistent"
```