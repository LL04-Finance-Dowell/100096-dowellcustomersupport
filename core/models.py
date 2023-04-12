from django.db import models



class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    session_id = models.CharField(max_length=32, blank=False, null=False)
    organization = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    userID = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f'{self.session_id} - {self.is_staff}'




class Room(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=200, blank=True, null=True)
    room_id = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    authority_portfolio = models.ManyToManyField(Portfolio)
    company = models.CharField(max_length=200, blank=True, null=True)
    product = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.room_name} - {self.company}'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    message_id = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    author = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.room.room_name} - {self.author}'