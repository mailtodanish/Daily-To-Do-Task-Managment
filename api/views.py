from django.shortcuts import render
from projects.models import Activity, TaskComment, ProjectTask
from .serializers import ActivitySerializer, TaskCommentSerializer
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template import loader
import random
from rest_framework import status


class ActivityDone(APIView):
    '''
    API for make activity done.
    There would be button on Activity to make it done.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        record = get_object_or_404(Activity, pk=pk)
        Act = Activity.objects.get(pk=pk)
        Act.status = "Done"
        Act.save()
        return Response(Act.status)


class ScheduledActivityList(APIView):
    '''
    Get list of scheduled activity to create daily activities.
    Test Case - Done
    '''
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records = Activity.objects.exclude(Type="General").filter(status='Open')
        rec=[]
        for r in records:
            find_record =  Activity.objects.filter(parentActivityId=r.pk,status='Open',Type="General")
            if find_record.count() == 0:
                       rec.append(r)
        data = ActivitySerializer(rec, many=True).data
        return Response(data)

class ChildActivityList(APIView):
    '''
    Get list of child activity of scheduled activity
    Test Case - 
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        records = Activity.objects.filter(parentActivityId=pk).order_by("-pk")
        data = ActivitySerializer(records, many=True).data
        return Response(data)


class RevisionItem(APIView):
    '''
    used: Load Revision Item button on Home Page to revise
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records = TaskComment.objects.all().order_by('updated')[1]
        data = TaskCommentSerializer(records).data
        return Response(data)


class RevisionItemUpdate(APIView):
    '''
    used : NextRevisionItem button on home page
    It only updates updated column of model.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = TaskComment.objects.get(pk=pk)
        comment.updated = timezone.now()
        comment.save()
        return Response("Success")


class RevisionItemofTheDay(APIView):
    '''
    It has been used in schedules activity to mail open activities
    Test Case - Done
    Status - Completed
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            dt = timezone.now()
            queryset = Activity.objects.filter(
                scheduled__lte=dt, Type='General').exclude(
                    status='Done').order_by('-scheduled')
            html_message = loader.render_to_string(
                'api/mail_template.html', {'Activities': queryset})
            email = EmailMessage('Task of the day',
                                 html_message, to=['mailtodanish@gmail.com'])
            email.content_subtype = "html"
            email.send()
            return Response("Success")
        except Exception as e:
            return Response(
                {"detail": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentsofTheDay(APIView):
    '''
    It has been used in schedules activity to mail 5 revision items
    Test Case - Done
    Status : Completed.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            queryset = TaskComment.objects.all()
            count = queryset.count()
            object_list = []
            while len(object_list) < 5:
                pk = random.randint(1, count-1)
                object_list.append(queryset[pk])
            domain = request.build_absolute_uri('/')[:-1]
            html_message = loader.render_to_string(
                'api/revision_items.html', {'items': object_list,
                                            'domain': domain})
            email = EmailMessage('Revision Items of the day ',
                                 html_message, to=['mailtodanish@gmail.com'])
            email.content_subtype = "html"
            email.send()
            return Response("Success")
        except Exception as e:
            return Response(
                {"detail": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
