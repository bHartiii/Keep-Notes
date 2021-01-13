from django.shortcuts import render
from Notes.serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer
from Notes.permissions import IsOwner
from Notes.models import Notes, Labels
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import status
import logging
import json
import redis_cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
logger = logging.getLogger('django')

class CreateAndListNotes(generics.ListCreateAPIView):
    """
        API to create and list notes for current logged in user
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

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
        return self.queryset.filter(owner=owner, isArchive=False, isDelete=False)   
         

class NoteDetails(generics.RetrieveUpdateDestroyAPIView):
    """ API views to retrieve, update, and delete note by id for requested user """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_update(self,serializer):
        """ Save notes model instance with updated values """
        owner = self.request.user
        note = serializer.save(owner=owner)
        a=cache.set(str(owner)+"-notes-"+str(note.id), note)
        logger.info(a)
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
            queryset = self.queryset.filter(owner=owner, isDelete=False, id=self.kwargs[self.lookup_field])
            logger.info("updated note data is coming form DB")
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
            

    def perform_destroy(self, instance):
        owner = self.request.user
        cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        instance.delete()


class CreateAndListLabels(generics.ListCreateAPIView):
    """ API views for list and create labels for logged in user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    
    def perform_create(self,serializer):
        """ Create label instance with owner and validated data by serializer and """
        label = serializer.save(owner=self.request.user)
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
        cache.set(str(owner)+"-labels-"+str(label.id), label)
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
            queryset = self.queryset.filter(owner=owner, id=self.kwargs[self.lookup_field])
            logger.info("updated label data is coming form DB")
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
        a=cache.set(str(owner)+"-notes-"+str(note.id), note)
        logger.info(a)
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
        note = serializer.save(owner=owner)
        if note.isDelete==True:
            cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        else:
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), note)
        logger.info("udated trashed note data is set")
        return note
        

    def get_queryset(self):
        """ Get the current delete field value of a note for given id """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info(queryset)
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
    
    def get_queryset(self):
        """ Filetr the queryset by isDelete field and owner id """
        owner = self.request.user
        return self.queryset.filter(owner=owner, isDelete=True)


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


class SearchNote(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self, queryset=None):
        owner = self.request.user
        if queryset:
            title_filter = Notes.objects.filter(title__contains=queryset)
            content_filter = Notes.objects.filter(content__contains=queryset)
            filter_cache = cache.get(queryset)
            if filter_cache:
                notes = filter_cache
                logger.info("data is coming from cache")
            elif title_filter:
                notes = title_filter
                cache.set(queryset, title_filter)
            elif content_filter :
                notes = content_filter
                cache.set(queryset, content_filter)
            else:
                notes = None
        else:
            notes = self.queryset
        return notes

    def get(self, request):
        queryset = request.GET.get('search')
        if queryset:
            note = self.get_queryset(queryset)
        else:
            note = self.get_queryset()
        serializer = NotesSerializer(note, many=True)
        return Response({'response_data':serializer.data}, status=status.HTTP_200_OK)










        