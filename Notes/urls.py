from django.urls import path
from django.conf.urls import url
from Notes.views import CreateAndListNotes, NoteDetails, DeleteNote, CreateAndListLabels, LabelDetails,  ArchiveNote, TrashUntrash, ArchiveNotesList, TrashList, AddLabelsToNote, ListNotesInLabel, SearchNote, AddCollaborator



urlpatterns = [
    path('notes/',CreateAndListNotes.as_view() , name='notes'),
    path('note/<int:id>',NoteDetails.as_view() , name='note'),
    path('delete-note/<int:id>', DeleteNote.as_view(), name='delete-note'),
    path('labels/',CreateAndListLabels.as_view() , name='labels'),
    path('label/<int:id>',LabelDetails.as_view() , name='label'),
    path('archive-note/<int:id>', ArchiveNote.as_view(), name='archive-note'),
    path('note-to-trash/<int:id>', TrashUntrash.as_view(), name='note-to-trash'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('trash-list/',TrashList.as_view(), name='trash-list'),
    path('add-label/<int:note_id>', AddLabelsToNote.as_view(), name='add-label'),
    path('list-notes-in-label/<int:id>', ListNotesInLabel.as_view(), name='list-notes-in-label'),
    path('search/', SearchNote.as_view(), name='search'),
    path('collaborator/<int:note_id>', AddCollaborator.as_view(), name='collaborator'),
]
