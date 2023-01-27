from django.db import models



class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    organization = models.CharField(max_length=200, blank=True, null=True)



class Room(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=200, blank=True, null=True)
    room_id = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    authority_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)

    def str(self):
        return f'{self.room_name} - {self.organization}'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    message_id = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    author = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)

    def str(self):
        return f'{self.room.room_name} - {self.author}'