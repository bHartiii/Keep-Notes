from django.urls import path
from django.conf.urls import url
from Notes.views import NotesListAPIView, NotesDetailsAPIView, NotesListAPIView, ArchiveNotesList, ArchiveNoteAPIView



urlpatterns = [
    path('notes/',NotesListAPIView.as_view() , name='notes'),
    path('<int:id>',NotesDetailsAPIView.as_view() , name='note'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('archive/<int:id>', ArchiveNoteAPIView.as_view(), name='archive'),
]
