import django_filters
import subprocess
import uuid
import os, sys
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from PyPDF2 import PdfFileReader
from netaddr import IPNetwork
from datetime import datetime
from rest_framework import viewsets, filters, permissions, parsers
from django.contrib.auth.models import User, Group
from APImpServ import models, serializers
from ImpServ import settings as st

# ViewSets define the view behavior

class UserFilter (django_filters.FilterSet):
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter

class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = models.UserProfile
        fields = ['id', 'user', 'user_type']

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserProfileFilter 

class PrinterFilter(django_filters.FilterSet):
    class Meta:
        model = models.Printer
        fields = ['id', 'name', 'uri', 'color', 'network', 'paper_size', 'description']

class PrinterViewSet(viewsets.ModelViewSet):
    queryset = models.Printer.objects.all()
    serializer_class = serializers.PrinterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PrinterFilter 

class UserTypeFilter(django_filters.FilterSet):
    class Meta:
        model = models.UserType
        fields = ['id', 'type_name', 'default']

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = models.UserType.objects.all()
    serializer_class = serializers.UserTypeSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserTypeFilter 

class QuotaFilter(django_filters.FilterSet):
    class Meta:
        model = models.Quota
        fields = ['id', 'printer', 'user_type', 'quota']

class QuotaViewSet(viewsets.ModelViewSet):
    queryset = models.Quota.objects.all()
    serializer_class = serializers.QuotaSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = QuotaFilter

class UserQuotaFilter(django_filters.FilterSet):
    class Meta:
        model = models.UserQuota
        fields = ['id', 'user', 'printer', 'quota', 'month', 'year']

class UserQuotaViewSet(viewsets.ModelViewSet):
    queryset = models.UserQuota.objects.all()
    serializer_class = serializers.UserQuotaSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserQuotaFilter

class LogsFilter(django_filters.FilterSet):
    class Meta:
        model = models.Logs
        fields = ['id', 'user', 'printer', 'creation_date', 'n_pages']

class LogsViewSet(viewsets.ModelViewSet): 
    queryset = models.Logs.objects.all()
    serializer_class = serializers.LogsSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = LogsFilter

class PrintSessionFilter(django_filters.FilterSet):
    class Meta:
        model = models.PrintSession
        fields = ['id', 'user', 'session', 'date']

class PrintSessionViewSet(viewsets.ModelViewSet): 
    queryset = models.PrintSession.objects.all()
    serializer_class = serializers.PrintSessionSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PrintSessionFilter

class PrintViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def post(self, request, format=None):
        uploaded_file = request.FILES['file_data']
        username_ = request.POST.get('username')
        passwd = request.POST.get('passwd')
          
        process = subprocess.Popen(["/bin/bash", "{0}/APImpServ/scripts/auth.sh".format(st.BASE_DIR), username_, passwd])
        streamdata = process.communicate()[0]
        rc = process.returncode
        
        if rc == 1:
            data = {'message': 'Login failed'}
            return Response(data, status=HTTP_403_FORBIDDEN)
        
        elif rc == 0:
            uuid_ = uuid.uuid4
            filename = '{0}/APImpServ/tmp/{1}.pdf'.format(st.BASE_DIR, uuid_)
            with open(filename, 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
        
            reader = PdfFileReader(open(filename, 'rb'))
            num_pages = reader.getNumPages()

            user_ = models.UserProfile.objects.get(user__username=username_)
            ip_client = request.META.get('REMOTE_ADDR')

            all_printers = models.Printer.objects.all()
            printers = []
            for prt in all_printers:

                ip, network = str(prt.network).split('/')
                printer_ip = IPNetwork(prt.network)
                client_ip_net = ip_client + '/' + network
                client_ip = IPNetwork(client_ip_net)

                if not models.UserQuota.objects.filter(printer=prt, user=user_):
                    quota_ = models.Quota.objects.get(printer=prt, user_type=user_.user_type).quota
                    models.UserQuota.objects.create(user=user_, printer=prt, quota=quota_)
                else:
                    quota_ = models.Quota.objects.get(printer=prt, user_type=user_.user_type).quota
                    user_quota_ = models.UserQuota.objects.get(printer=prt, user=user_)
                    if user_quota_.month != datetime.now().month or user_quota_.year != datetime.now().year:
                        models.UserQuota.objects.filter(printer=prt, user=user_).update(month=datetime.now().month, year=datetime.now().year, quota=quota_)
        
                if (client_ip.network == printer_ip.network) and (num_pages <= int('0' + models.UserQuota.objects.get(printer=prt, user=user_).quota)):
                    printers.append({"name": prt.name, "description": prt.description, "quota": models.UserQuota.objects.get(printer=prt, user=user_).quota})
        
            session_ = models.PrintSession.objects.create(user=user_).session
            os.renames('{0}/APImpServ/tmp/{1}.pdf'.format(st.BASE_DIR, uuid_), '{0}/APImpServ/tmp/{1}.pdf'.format(st.BASE_DIR, session_))
    
            data_ = [{"session": session_, "printers": printers}]

            serializer = serializers.PrintSerializer(data=data_, many=True)
            serializer.is_valid()
            return Response(serializer.validated_data)

        return Response({'message': 'Login script failed'}, status=HTTP_403_FORBIDDEN)

    def list(self, request, format=None):
        return Response(data={'message': 'This function only works via POST request'})

class PrintOnViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        session_ = request.POST.get('session')
        printer_ = request.POST.get('printer')

        prt = models.Printer.objects.get(id=printer_)

        process = subprocess.Popen(["lp", "-d", 'Virtual_PDF_Printer', "{0}/APImpServ/tmp/{1}.pdf".format(st.BASE_DIR, session_)])
        streamdata = process.communicate()[0]
        rc = process.returncode

        os.remove('{0}/APImpServ/tmp/{1}.pdf'.format(st.BASE_DIR, session_))
        models.PrintSession.objects.get(session=session_).delete()

        if rc != 0:
            data_ = {'message': 'Print action failed'}
            return Response(data=data_, status=HTTP_403_FORBIDDEN)

        else:
            data_ = {'message': 'Print successful'}
            return Response(data=data_, status=HTTP_200_OK)
        

    def list(self, request, format=None):
        return Response(data={'This function only works via POST request'})


