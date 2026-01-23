from django.urls import path
from .import views


urlpatterns = [
    #notes
    path('', views.home, name='home'),
    path('notes', views.note, name='note'),
    path('notes/<int:pk>/', views.delete_note, name='delete_note'),
    path('note_detail/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),

    #homework
    path('homework/', views.homework, name='homework'),
]
