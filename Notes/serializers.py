from rest_framework import serializers
from Notes.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete',]
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True},}  

class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields=['name']

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

class AddNotesInLabelsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields=['name']  

class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    label =AddNotesInLabelsSerializer(many=True, queryset=Labels.objects.all())
    class Meta:
        model = Notes
        fields=['title','content','owner','label']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}
        def validate(self, attrs):
            labels = attrs.get('label','')
            owner = attrs.get('owner','')
            title= attrs.get('title','')
            content = attrs.get('content','')
            return attrs


