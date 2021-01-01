from rest_framework import serializers
from Notes.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete']
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True}}  

    
class AddLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields='__all__'

class CreateLabelSerializer(serializers.ModelSerializer):
    notes = NotesSerializer(required=False, default=None)
    class Meta:
        model = Labels
        fields=['name','notes']
        def validate(self, attrs):
            name = attrs.get('name','')
            return attrs

        def create(self, validated_data):
            note_data= validated_data.pop('notes')
            label = Labels.objects.create(**validated_data)
            return label

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

