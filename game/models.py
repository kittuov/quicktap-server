from django.db import models
from django.contrib.auth.models import User

from djwebsockets.server import WebSocketServer

# Create your models here.
AVATARS = [
    (0, "ZERO"),
    (1, "ONE"),
    (2, "TWO"),
    (3, "THREE"),
    (4, "FOUR"),
    (5, "FIVE"),
    (6, "SIX"),
    (7, "SEVEN"),
    (8, "EIGHT"),
    (9, "NINE")
]


class Profile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    image = models.IntegerField(choices=AVATARS, default=0)
    firstName = models.CharField(max_length=30)
    ws_id = models.IntegerField(null=True)
    lastName = models.CharField(max_length=30)
    won = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def login(self, request):
        request.session["profile-id"] = self.pk


class Move(models.Model):
    user = models.ForeignKey(Profile)
    x = models.IntegerField(verbose_name="Horizontal Grid Number")
    y = models.IntegerField(verbose_name="Vertical Grid Number")
    attempt = models.IntegerField(verbose_name="Situation of attempt")


class Game(models.Model):
    users = models.ManyToManyField(Profile, blank=True)
    dimen = models.IntegerField(null=True, blank=True)
    timeGap = models.IntegerField(default=3)
    isFinished = models.BooleanField(default=False)
    isStarted = models.BooleanField(default=False)
    timeCreated = models.DateTimeField(auto_now=True)
    room = models.CharField(max_length=10)

    def __str__(self):
        return str(self.pk)

    def add_user(self, profile):
        self.users.add(profile)
        self.save()

    def start_game(self):
        if self.users.all().count() >= 2 and self.dimen is not None:
            self.isStarted = True
            self.save()
            return True
        else:
            return False

    def publish(self, message):
        for user in self.users.all():
            ws = WebSocketServer.get_websocket_by_id(user.ws_id)
            ws.send(message)

