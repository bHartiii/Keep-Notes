from rest_framework import serializers
from Notes.models import Notes, Labels
from authentication.models import User
from rest_framework.renderers import JSONRenderer

class NotesSerializer(serializers.ModelSerializer):
    collaborator = serializers.StringRelatedField()
    class Meta:
        model= Notes
        fields=['title','content','label','isArchive','isDelete','owner_id','collaborator']
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True}, 'owner_id': {'read_only': True}, 'collaborator': {'read_only': True}, 'label': {'read_only': True}}  

        def validate(self, data):
            title = data.get('title','')
            content = data.get('content','')
            return data

class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields=['name','owner']
        extra_kwargs = {'owner':{'read_only':True}}

class ArchiveNotesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete','owner_id']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True}, 'isDelete': {'read_only': True},'owner_id': {'read_only': True}}   

class TrashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isDelete','isArchive','owner_id']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True},'isArchive':{'read_only':True}, 'owner_id': {'read_only': True}}   


class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    label =serializers.PrimaryKeyRelatedField(many=True, queryset=Labels.objects.all())
    class Meta:
        model = Notes
        fields=['title','content','label','owner']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}


class AddCollaboratorSerializer(serializers.ModelSerializer):
    collaborator = serializers.EmailField()
    class Meta:
        model = Notes
        fields = ['title','content','label','owner','collaborator'] 
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True},'label': {'read_only': True}}

