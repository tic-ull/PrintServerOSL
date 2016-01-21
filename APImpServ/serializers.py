from django.contrib.auth.models import User
from rest_framework import serializers
from APImpServ import models

#Serializers define the API representation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'is_staff')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'user', 'user_type')

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Printer
        fields = ('id', 'name', 'uri', 'color', 'network', 'paper_size', 'description')

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserType
        fields = ('id', 'type_name', 'default')

class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quota
        fields = ('id', 'printer', 'user_type', 'quota')

class UserQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserQuota
        fields = ('id', 'user', 'printer', 'quota', 'month', 'year')

class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Logs
        fields = ('id', 'user', 'printer', 'creation_date', 'n_pages')

class PrintSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrintSession
        fields = ('id', 'user', 'session', 'date')

class PrintersSerializer(serializers.Serializer):
    quota = serializers.CharField(max_length=4)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField()

class PrintSerializer(serializers.Serializer):
    session = serializers.UUIDField()
    printers = PrintersSerializer(many=True)

