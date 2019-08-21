'''
Classe helper para unificar o modo de comunicação com um broker solace

Tipos de mensagens:

* Topic: mensagem de notificação sem persistência. Os clientes precisam estar on-line para receber.
* Queue: mensagem enfileirada. Os clientes podem receber as mensagens assim que estiverem on-line.

Funções gerais: 

* Enviar mensagem para um topic
* Enviar mensagem para um queue
* Receber mensagem de um topic
* Receber mensagem de um queue

'''
import optparse
from proton.handlers import MessagingHandler
from proton.reactor import Container


class SolaceHelper(MessagingHandler):

    def __init__(self, url, username, password):
        super(SolaceHelper, self).__init__()
        self.url = url        
        self.username = username
        self.password = password
        self.message_durability = True
        self.queues = []    # Queues utilizados
        self.topic = []     # Topics utilizados
        self.conn = None    # Conexão default

    def SendToTopic(self, topic: str, datum):
        '''
        Enviar mensagem para um topic
        '''

    def SendToQueue(self, datum):
        '''
        Enviar mensagem para um queue
        '''

    def ReceiveFromTopic(self, topic: str):
        '''
        Receber uma mensagem de um topic
        '''

    def ReceiveFromQueue(self):
        '''
        Receber uma mensagem de um queue
        '''

    def on_start(self, event):
        if self.username:
            conn = event.container.connect(
                url=self.url, user=self.username, password=self.password, allow_insecure_mechs=True)
        else:
            conn = event.container.connect(url=self.url)

        if conn:
            event.container.create_sender(conn, target=self.queue)
            event.container.create_receiver(conn, source=self.queue)

#    def on_sendable(self, event):
