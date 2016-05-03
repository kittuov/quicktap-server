import json

from rest_framework.renderers import JSONRenderer

from djwebsockets.decorator import Namespace
from djwebsockets.websocket import BaseWSClass
from djwebsockets.mixins.wsgi import WSGIMixin

from .models import Game, Profile
from api.serializer import ProfileSerializer, GameSerializer


@Namespace("/room/")
class GameSocket(WSGIMixin, BaseWSClass):
    rooms = {}

    @classmethod
    def on_connect(cls, websocket, path):
        print("fuckoff")
        pId = websocket.session.get("profile-id")
        if pId is None:
            websocket.send("{'error': 'Not Authenticated'}")
            websocket.close()
            return
        profile = Profile.objects.get(id=pId)
        profile.ws_id = websocket.id
        profile.save()

    @classmethod
    def on_message(cls, websocket, message):
        print(message)
        pid = websocket.session.get("profile-id")
        profile = Profile.objects.get(id=pid)
        try:
            damp = json.loads(message)
        except json.JSONDecodeError:
            damp = {}
            print("error Decoding JSON")
        # registering to a room
        # adding a user to a room
        if not hasattr(websocket, "room"):
            room = damp.get("room")
            if room is None:
                websocket.send("{'error': 'Not Yet regiesterd in a room'}")
                websocket.close()
                return
            setattr(websocket, "room", room)
            if cls.rooms.get(room) is None:
                cls.rooms[room] = Game(room=room)
                cls.rooms[room].save()
            game = cls.rooms[room]
            if game.isStarted:
                websocket.send("{'error':'a game is in progress in that socket'}")
                websocket.close()
                return
            user_str = JSONRenderer().render(ProfileSerializer(profile).data)
            game.publish("{\"add_user\":"+user_str.decode("utf-8")+"}")
            game.add_user(profile)
            game.save()
            users_str = JSONRenderer().render(ProfileSerializer(game.users.all(), many=True).data).decode("utf-8")
            websocket.send("{\"users\": "+users_str+",\"room\":\""+room+"\"}")
        elif damp.get("ready_set") is not None:
            size = damp.get("ready_set")
            game = cls.rooms.get(websocket.room)
            if 3 <= size <= 8:
                game.dimen = size
                game.save()
                game.start_game()
                game.publish("{\"ready_set\":\"{}\"}".format(JSONRenderer.render(GameSerializer(game).data)))
            return

            # TODO: game initiation

    @classmethod
    def on_close(cls, websocket):
        try:
            profile = Profile.objects.get(ws_id=websocket.id)
            profile.ws_id = None
            profile.save()
        except Profile.DoesNotExist:
            return

        if hasattr(websocket, "room"):
            room = websocket.room
            game = cls.rooms[room]
            if not game.isStarted:
                game.users.remove(profile)
                game.save()
                if game.users.count() == 0:
                    cls.rooms.__delitem__(room)
                    game.delete()
                    return
                game.publish("{\"remove_user\":"+str(profile.id)+"}")
