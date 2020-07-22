from rest_framework import viewsets
from projects.models import Activity, ProjectTask
from .serializers import ActivitySerializer, TaskSerializer
from rest_framework import authentication, permissions


class ActivityViewSet(viewsets.ModelViewSet):
    '''
     ActivityRouter - Test Case - Done
     '''
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (permissions.IsAuthenticated,)
