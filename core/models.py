from django.db import models



# class Portfolio(models.Model):
#     portfolio_name = models.CharField(max_length=200, blank=True, null=True)
#     is_staff = models.BooleanField(default=False)
#     session_id = models.CharField(max_length=32, blank=False, null=False)
#     organization = models.CharField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return f'{self.session_id} - {self.is_staff}'


class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    session_id = models.CharField(max_length=32, blank=False, null=False)
    organization = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=False, null=False, default='RT') #
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    userID = models.CharField(max_length=200, blank=True, null=True)
    dowell_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.session_id} - {self.is_staff}'


class Room(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=200, blank=True, null=True)
    room_id = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    authority_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    sub_product = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.room_name} - {self.company}'

    def jsonify_room(self):
        return {'room_name': self.room_name, 'room_id': self.room_id, 'active': self.active, 'company': self.company, 'product': self.product}



from django.utils.translation import gettext_lazy as _RT__
class MessageType(models.TextChoices):
	TEXT = "TEXT", _RT__("Text")
	IMAGE = "IMAGE", _RT__("Image")


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    message_id = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    author = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    side = models.BooleanField(default=False)# false for sender , true for reciever
    message_type = models.CharField(max_length=10, choices=MessageType.choices, default=MessageType.TEXT)

    def __str__(self):
        return f'{self.room.room_name} - {self.author}'