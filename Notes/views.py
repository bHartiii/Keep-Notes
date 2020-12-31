from django.shortcuts import render
from Notes.serializers import NotesSerializer, ArchiveNotesSerializer
from Notes.permissions import IsOwner
from Notes.models import Notes
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

# Create your views here.

class NotesListAPIView(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication


    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user,isArchive=False, isDelete=False)


class NotesDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user,isDelete=False)

class ArchiveNotesList(generics.ListAPIView):
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user,isArchive=True, isDelete=False)

class ArchiveNoteAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"
 
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user,isDelete=False)

