from rest_framework import serializers
from Notes.models import Notes

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model= Notes
        fields=['date','title','content']