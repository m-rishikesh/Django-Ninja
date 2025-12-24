import json
from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):

#     def connect(self):
#         self.accept()
#         # give a welcome message on connecting
#         self.send(text_data="<p>Welcome to Websocket</p>")

#     def disconnect(self,close_code):
#         print("websocket closed :)",close_code)

#     def receive(self,text_data):
#         json_payload = json.loads(text_data)
#         print("json_payload : ",json_payload)
#         message = json_payload["message"]
#         self.send(text_data=f"<p>Message: {message}</p>")
connected_user = {}
client_id = 0
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        global client_id
        client_id = client_id+1
        self.room_name = 'lobby'
        self.group_name = 'chat_'+ self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        connected_user[self.channel_name] = "client_"+str(client_id)
        self.accept()

    def disconnect(self,close_code):
        global client_id
        if client_id > 0:
            client_id = client_id -1
            print("client_disconnect: ",client_id)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self,text_data):
        json_payload = json.loads(text_data)
        msg = json_payload["message"]
        username = json_payload["username"]

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'broadcast_msg',
                'message':msg,
                'username':username,
                'channel_name':self.channel_name,
            }
        )

    def broadcast_msg(self,event):
        if self.channel_name == event['channel_name']:
            return
        message = event['message']
        self.send(text_data=f"<p><b>{event['username']}:</b> {message}")
