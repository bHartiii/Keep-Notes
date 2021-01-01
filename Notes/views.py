from django.shortcuts import render
from Notes.serializers import NotesSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelSerializer, CreateLabelSerializer
from Notes.permissions import IsOwner, IsLabel
from Notes.models import Notes, Labels
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

# Create your views here.

class NotesListAPIView(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user,isArchive=False, isDelete=False)


class NotesDetails(generics.RetrieveUpdateDestroyAPIView):
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

class ArchiveNote(generics.RetrieveUpdateAPIView):
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isDelete=False)
 
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    

class Trash(generics.RetrieveUpdateAPIView):
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

 
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class TrashList(generics.ListAPIView):
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class=TrashSerializer
    queryset = Notes.objects.all()
    lookup_field='id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isDelete=True)

class CreateLabel(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateLabelSerializer
    queryset = Labels.objects.all()

    def perform_create(self,serializer):
        serializer.is_valid(raise_exception=True)
        label=serializer.save(owner=self.request.user)
        data = serializer.data
        note_details=data['notes']
        notes=Notes.objects.create(label=label,title=note_details['title'], content=note_details['content'],owner=self.request.user)
        notes.save()
        return label
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class AddLabelsToNotes(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddLabelSerializer

