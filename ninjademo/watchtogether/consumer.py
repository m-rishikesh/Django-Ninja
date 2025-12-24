from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time
class VideoConsumer(AsyncWebsocketConsumer):
    room_state = {}
    async def connect(self):
        self.room_name = "watch_party"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        if self.room_name in self.room_state:
            state = self.room_state[self.room_name]
            currentseconds = state['seconds']
            if state['playing']:
                time_elapsed = time.time() - state['last_update']
                currentseconds = currentseconds + time_elapsed
            await self.send(text_data=json.dumps({
                'action':'sync',
                'seconds':currentseconds,
                'playing':state['playing']
            }))

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )

    async def receive(self,text_data):
        json_payload = json.loads(text_data)

        self.room_state[self.room_name] = {
            'seconds':json_payload['seconds'],
            'playing':(json_payload['action'] == 'play'),
            'last_update':time.time()
        }
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type':'video_sync',
                'action':json_payload['action'],
                'seconds':json_payload['seconds'],
            }
        )

    async def video_sync(self,event):
        await self.send(text_data = json.dumps({
            'action':event['action'],
            'seconds':event['seconds']
        }))
