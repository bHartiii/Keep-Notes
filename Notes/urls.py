from django.urls import path
from django.conf.urls import url
from Notes.views import CraeteAndListNotes, NoteDetails, CreateAndListLabels, LabelDetails,  ArchiveNote, NoteToTrash, ArchiveNotesList, TrashList, AddLabelsToNote, ListNotesInLabel



urlpatterns = [
    path('notes/',CraeteAndListNotes.as_view() , name='notes'),
    path('note/<int:id>',NoteDetails.as_view() , name='note'),
    path('labels/',CreateAndListLabels.as_view() , name='labels'),
    path('label/<int:id>',LabelDetails.as_view() , name='label'),
    path('archive-note/<int:id>', ArchiveNote.as_view(), name='archive-note'),
    path('note-to-trash/<int:id>', NoteToTrash.as_view(), name='note-to-trash'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('trash-list/',TrashList.as_view(), name='trash-list'),
    path('add-label/<int:id>', AddLabelsToNote.as_view(), name='add-label'),
    path('list-notes-in-label/<int:id>', ListNotesInLabel.as_view(), name='list-notes-in-label'),
]
