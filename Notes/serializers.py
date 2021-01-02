from rest_framework import serializers
from Notes.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete','label']
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True}}  


class CreateAndListLabelSerializer(serializers.ModelSerializer):
    notes = NotesSerializer(required=False)
    class Meta:
        model = Labels
        fields=['name','id','notes']
        extra_kwargs = {'id': {'read_only': True}}
        def validate(self, attrs):
            name = attrs.get('name','')
            return attrs

        def create(self, validated_data):
            note_data= validated_data.pop('notes')
            label = Labels.objects.create(**validated_data)
            return label

class AddLabelSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Notes
        fields= ['title','content','label']

        def validate(self, attr):
            label = attr.get('label','')
            return attrs

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

