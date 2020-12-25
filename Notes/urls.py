from django.urls import path
from django.conf.urls import url
from Notes.views import NotesListAPIView, NotesDetailsAPIView



urlpatterns = [
    path('notes/',NotesListAPIView.as_view() , name='notes'),
    path('<int:id>',NotesDetailsAPIView.as_view() , name='note'),
    
]
