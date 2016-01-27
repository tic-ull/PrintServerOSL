import uuid
from django.db import models
from django.db.models import Model, URLField, UUIDField, DateTimeField, CharField, BooleanField, TextField
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings as st

# Create your models here.
class UserProfile(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(st.AUTH_USER_MODEL)
    user_type = models.ForeignKey('UserType', related_name="users")

    def __str__(self):
        return '%s' % self.user.get_username()

class Printer(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=50)
    uri = URLField()
    color = BooleanField(default=False)
    paper_size = CharField(max_length=5)
    description = TextField()
    network = CharField(max_length=20, default="0.0.0.0/24")

    def __str__(self):
        return '%s' % self.name

class UserType(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = CharField(max_length=50)
    default = BooleanField(default=False)

    def __str__(self):
        return '%s' % self.type_name

class Quota(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    printer = models.ForeignKey('Printer')
    user_type = models.ForeignKey('UserType', related_name="Quotas")
    #La cuota será un número, que será el numero de página a imprimir por mes y usuario.
    quota = CharField(max_length=4)

class UserQuota(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('UserProfile')
    printer = models.ForeignKey('Printer', related_name="printers")
    quota = CharField(max_length=4)
    month = CharField(max_length=2, default=date.today().month)
    year = CharField(max_length=4, default=date.today().year)    

    def __str__(self):
        return '%s' % self.quota

class Logs(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('UserProfile')
    printer = models.ForeignKey('Printer')
    creation_date = DateTimeField(auto_now=True)
    n_pages = CharField(max_length=3)

class PrintSession(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('UserProfile')
    session = UUIDField(default=uuid.uuid4, editable=False)
    date = DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "date"
