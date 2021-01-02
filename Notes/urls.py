from django.urls import path
from django.conf.urls import url
from Notes.views import NotesListAPIView, NotesDetails, NotesListAPIView, ArchiveNotesList, ArchiveNote, TrashList, Trash, CreateAndListLabel, AddLabelsToNotes



urlpatterns = [
    path('notes/',NotesListAPIView.as_view() , name='notes'),
    path('<int:id>',NotesDetails.as_view() , name='note'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('archive/<int:id>', ArchiveNote.as_view(), name='archive'),
    path('trash-note/<int:id>', Trash.as_view(), name='trash'),
    path('trash-list/',TrashList.as_view(), name='trash-list'),
    path('create-label/', CreateAndListLabel.as_view(), name='craete-label'),
    path('add-label/<int:id>', AddLabelsToNotes.as_view(), name='add-label')
]
