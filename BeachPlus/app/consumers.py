import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from app.models import ChatRoom,RoomMessage,SingleChatRoom,SingleRoomMessage,Profiles
import django 

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        chatType = self.scope['url_route']['kwargs']['chatType']
        if chatType=='singleChat':
            self.user1=self.scope['url_route']['kwargs']['token_user_id']
            self.user2=self.scope['url_route']['kwargs']['other_user_id']
            if int(self.user1) > int(self.user2):
                self.roomname = f'{self.user1}-{self.user2}'
            else:
                self.roomname = f'{self.user2}-{self.user1}'
        
            self.room_group_name = self.roomname
            print(self.room_group_name)
            if not SingleChatRoom.objects.filter(roomname=self.roomname).exists():
                u1=Profiles.objects.get(User=self.user1)
                u2=Profiles.objects.get(User=self.user2)
                SC=SingleChatRoom.objects.create(roomname=self.roomname,user1=u1,user2=u2)
                self.SC=SC
            else:
                SingleChatRoom.objects.filter(roomname=self.roomname).update(DateAdded=django.utils.timezone.now())

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        room=SingleChatRoom.objects.get(roomname=self.room_group_name)
        self.send(text_data=json.dumps({'type':'room_info','room_id':room.id}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json['message']
        self.user_messaging = text_data_json['user']
        messageType = text_data_json['messageType']
        SingleChatRoom.objects.filter(roomname=self.room_group_name).update(DateAdded=django.utils.timezone.now())
        
        room=SingleChatRoom.objects.get(roomname=self.room_group_name)
        u=Profiles.objects.get(User=self.user_messaging)
        s=SingleRoomMessage.objects.create(Room=room,User=u,content=self.message,messageType=messageType)
        
        
        self.timestamp_this=s.timestamp
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.message,
                'content':self.message,
                'timestamp':self.timestamp_this,
                'User_id':self.user_messaging,
            }
        )
        
    # def send_room(self, event):
    #     room_id = event['room_id']
        
    #     self.send(text_data=json.dumps({
    #         'type':'room',
    #         'room_id':room_id,
    #     }))
    
    def chat_message(self, event):
        message = event['message']
        user_messaging = event['User_id']
        t=event['timestamp']
        str_t=t.strftime("%Y-%m-%dT%H:%M:%S.000000Z")
        # SingleChatRoom.objects.filter(roomname=event['roomname']).update(DateAdded=django.utils.timezone.now())
        
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'content':message,
            'timestamp':str_t,
            'User_id':user_messaging,
        }))
        
    def disconnect(self, event):
        print('disconnect', event)    
        

@database_sync_to_async
def single_room_exists(roomname):
    r=SingleChatRoom.objects.filter(roomname=roomname).exists()
        
@database_sync_to_async
def create_single_room(roomname,user1,user2):
    u1=Profiles.objects.get(User=user1)
    u2=Profiles.objects.get(User=user2)
    SingleChatRoom.objects.create(roomname=roomname,user1=u1,user2=u2)
    
@database_sync_to_async
def save_single_message(room,user,message):
    roomname=SingleChatRoom.objects.get(roomname=room)
    u=Profiles.objects.get(User=user)
    SingleRoomMessage.objects.create(roomname=roomname,user=u,content=message)    

