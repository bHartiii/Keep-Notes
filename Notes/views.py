from django.shortcuts import render
from Notes.serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer
from Notes.permissions import IsOwner
from Notes.models import Notes, Labels
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


class CraeteAndListNotes(generics.ListCreateAPIView):
    """
        API to create and list notes for current logged in user
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        """ Create new note for user """        
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """ Get notes list owned by current logged in user """
        return self.queryset.filter(owner=self.request.user,isArchive=False, isDelete=False)


class NoteDetails(generics.RetrieveUpdateDestroyAPIView):
    """ API views to retrieve, update, and delete note by id for requested user """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_create(self,serializer):
        """ Save notes model instance with updated values """
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """ Get note for given id owned by user """
        return self.queryset.filter(owner=self.request.user,isDelete=False)

class CreateAndListLabels(generics.ListCreateAPIView):
    """ API views for list and create labels for logged in user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    
    def perform_create(self,serializer):
        """ Create label instance with owner and validated data by serializer and """
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """ List all labels qwned by user """
        return self.queryset.filter(owner=self.request.user)


class LabelDetails(generics.RetrieveUpdateDestroyAPIView):
    """ APIs to retrieve, update and delete labels by id for user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_create(self,serializer):
        """ Update label instance with validated data provided by serializer """
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """ Get label details for given label id owned by user """
        return self.queryset.filter(owner=self.request.user)

class ArchiveNote(generics.RetrieveUpdateAPIView):
    """ API to update archive field value of a note owned by user """
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        """ Get current archive field value of note """
        return self.queryset.filter(owner=self.request.user, isDelete=False)
 
    def perform_create(self,serializer):
        """ Update archive field with new boolean value given"""
        return serializer.save(owner=self.request.user)
    
class NoteToTrash(generics.RetrieveUpdateAPIView):
    """ API to update delete field value of note for given id so it can be moved to trash """
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        """ Get the current delete field value of a note for given id """
        return self.queryset.filter(owner=self.request.user)

 
    def perform_create(self,serializer):
        """ Update delete field value of note with value given by user """
        return serializer.save(owner=self.request.user)

class ArchiveNotesList(generics.ListAPIView):
    """ API to list all archived notes list for user """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        """ filter the queryset for isArchive field value and owner """
        return self.queryset.filter(owner=self.request.user,isArchive=True, isDelete=False)
    
class TrashList(generics.ListAPIView):
    """ API to get list of all trashed notes list for user """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class=TrashSerializer
    queryset = Notes.objects.all()

    def get_queryset(self):
        """ Filetr the queryset by isDelete field and owner id """
        return self.queryset.filter(owner=self.request.user, isDelete=True)

class AddLabelsToNote(generics.RetrieveUpdateAPIView):
    """ API to add available labels to notes of requested user """
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    serializer_class = AddLabelsToNoteSerializer
    queryset = Notes.objects.all()
    lookup_field="id"

    def perform_update(self,serializer): 
        """ Update label field of notes model """   
        return serializer.save(owner=self.request.user)


    def get_queryset(self):
        """ Get current details of note fetched by id """
        return self.queryset.filter(owner=self.request.user)

class ListNotesInLabel(generics.ListAPIView):
    """ API for list all notes in a given label """
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    serializer_class = AddLabelsToNoteSerializer
    queryset = Notes.objects.all()
    lookup_field='id'

    def get_queryset(self):
        """ Label is fetched by id """
        return self.queryset.filter(owner=self.request.user,label=self.kwargs[self.lookup_field])
