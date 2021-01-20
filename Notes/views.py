from django.shortcuts import render
from Notes.serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer,ListNoteInLabelSerializer, AddCollaboratorSerializer
from Notes.permissions import IsOwner, IsCollaborator
from Notes.models import Notes, Labels
from authentication.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from rest_framework import status
import logging
from datetime import datetime

logger = logging.getLogger('django')

class CreateAndListNotes(generics.ListCreateAPIView):
    """
        API to create and list notes for current logged in user
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsCollaborator)

    def perform_create(self,serializer):
        """ Create new note for user """ 
        owner = self.request.user
        note = serializer.save(owner=owner)
        cache.set(str(owner)+"-notes-"+str(note.id), note)
        if cache.get(str(owner)+"-notes-"+str(note.id)):
            logger.info("Data is stored in cache")
        return Response({'success':'New note is created!!'}, status=status.HTTP_201_CREATED)
    
    
    def get_queryset(self): 
        """ Get notes list owned by current logged in user """
        owner = self.request.user
        return self.queryset.filter(Q(owner=owner)|Q(collaborator=owner), Q(isArchive=False,isDelete=False))   
         

class NoteDetails(generics.RetrieveUpdateAPIView):
    """ API views to retrieve, update, and delete note by id for requested user """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsCollaborator)
    lookup_field="id"

    def perform_update(self,serializer):
        """ Save notes model instance with updated values """
        owner = self.request.user
        note = serializer.save()
        cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated note data is set")
        return note
        

    def get_queryset(self):
        """ Get note for given id owned by user """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated note data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(Q(owner=owner)|Q(collaborator=owner), Q(isArchive=False,isDelete=False))
            logger.info("updated note data is coming form DB")
            if queryset:
                cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
            

class DeleteNote(generics.DestroyAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    lookup_field="id"

    def perform_destroy(self, instance):
        owner = self.request.user
        cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        instance.delete()


class CreateAndListLabels(generics.ListCreateAPIView):
    """ API views for list and create labels for logged in user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        """ Create label instance with owner and validated data by serializer and """
        owner = self.request.user
        label = serializer.save(owner=owner)
        cache.set(str(owner)+"-labels-"+str(label.id), label)
        if cache.get(str(owner)+"-labels-"+str(label.id)):
            logger.info("Label data is stored in cache")
        return Response({'success':'New label is created!!'}, status=status.HTTP_201_CREATED)
    

    def get_queryset(self):
        """ List all labels qwned by user """
        owner = self.request.user
        return self.queryset.filter(owner=owner)


class LabelDetails(generics.RetrieveUpdateDestroyAPIView):
    """ APIs to retrieve, update and delete labels by id for user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_update(self,serializer):
        """ Update label instance with validated data provided by serializer """
        owner = self.request.user
        label = serializer.save(owner=owner)
        cache.set(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated label data is set")
        return label
    
    def get_queryset(self):
        """ Get label details for given label id owned by user """
        owner = self.request.user
        if cache.get(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated label data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(owner=owner)
            logger.info("updated label data is coming form DB")
            if queryset:
                cache.set(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset

    def perform_destroy(self, instance):
        owner = self.request.user
        cache.delete(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]))
        instance.delete()


class ArchiveNote(generics.RetrieveUpdateAPIView):
    """ API to update archive field value of a note owned by user """
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        """ Get current archive field value of note """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated archive notes data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(owner=owner,isDelete=False, id=self.kwargs[self.lookup_field])
            logger.info("updated archive note data is coming form DB")
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
        
 
    def perform_update(self,serializer):
        """ Update archive field with new boolean value given"""
        owner = self.request.user
        note = serializer.save(owner=owner)
        a=cache.set(str(owner)+"-notes-"+str(note.id), self.queryset.all())
        logger.info("udated archive note data is set")
        return note
    

class ArchiveNotesList(generics.ListAPIView):
    """ API to list all archived notes list for user """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        """ filter the queryset for isArchive field value and owner """
        return self.queryset.filter(owner=self.request.user,isArchive=True, isDelete=False)


class TrashUntrash(generics.RetrieveUpdateAPIView):
    """ API to update delete field value of note for given id so it can be moved to trash """
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_update(self,serializer):
        """ Update delete field value of note with value given by user """
        owner = self.request.user
        if serializer.validated_data['isDelete']==True:
            note = serializer.save(owner=owner, trashedAt=datetime.now())
        else:
            note = serializer.save(owner=owner, trashedAt=None)
        if note.isDelete==True:
            cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        else:
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated trashed note data is set")
        return note
        

    def get_queryset(self):
        """ Get the current delete field value of a note for given id """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated trashed note data is coming from cache")
            return queryset

        else:
            queryset = self.queryset.filter(owner=owner, id=self.kwargs[self.lookup_field])
            logger.info("updated trashed note data is coming form DB")
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
        

class TrashList(generics.ListAPIView):
    """ API to get list of all trashed notes list for user """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        """ Filetr the queryset by isDelete field and owner id """
        owner = self.request.user
        return self.queryset.filter(owner=owner, isDelete=True)


class AddLabelsToNote(generics.GenericAPIView):
    """ API to add available labels to notes of requested user """
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    serializer_class = AddLabelsToNoteSerializer

    def put(self, request, note_id):
        try:
            note = Notes.objects.get(id=note_id, owner=request.user)
        except Notes.DoesNotExist:
            return Response({'response':'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        label_name = serializer.data['label']
        try:
            label = Labels.objects.get(name=label_name, owner=self.request.user)
        except Labels.DoesNotExist:
            label = Labels.objects.create(name=label_name, owner=self.request.user)
        note.label.add(label.id)
        note.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListNotesInLabel(generics.ListAPIView):
    """ API for list all notes in a given label """
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    serializer_class = ListNoteInLabelSerializer
    lookup_field='label_id'

    def get_queryset(self):
        """ Label is fetched by id """
        return Labels.objects.get(id=self.kwargs[self.lookup_field],owner=self.request.user).notes_set.all()


class SearchNote(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,IsOwner)
    serializer_class = NotesSerializer    
    
    def get_queryset(self, queryset=None):
        notes = []
        owner = self.request.user
        if queryset:                
            searchlist = queryset.split(' ')
            for query in searchlist:
                if cache.get(query):
                    notes = cache.get(query)
                    logger.info("data is coming from cache")
                else:
                    notes = Notes.objects.filter(Q(title__icontains=query)|Q(content__icontains=query), Q(isArchive=False,isDelete=False))
                    if notes:
                        cache.set(query, notes)  
        return notes

    def get(self, request):
        queryset = request.GET.get('search')
        if queryset:
            note = self.get_queryset(queryset)
        else:
            return Response({'response':'Give some search string!!!'})
        serializer = NotesSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsCollaborator)
    serializer_class = AddCollaboratorSerializer
    
    def put(self, request ,note_id):
        note = Notes.objects.get(id=note_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        collaborator_email = serializer.validated_data['collaborator']
        try:
            collaborator = User.objects.get(email=collaborator_email)
        except:
            return Response({'This user email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if collaborator==request.user:
            return Response({'Detail': 'This email already exists!!!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note.collaborator.add(collaborator)
            note.save()
            return Response({'collaborator':collaborator_email}, status=status.HTTP_200_OK)

    
        






        