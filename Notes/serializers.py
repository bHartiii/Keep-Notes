from rest_framework import serializers
from Notes.models import Notes

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete']
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True}}   

class ArchiveNotesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isArchive']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True}}   

class TrashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isDelete','isArchive']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True},'isArchive':{'read_only':True}}   