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
    path('homework/update/<int:pk>/', views.update_homework, name='update_homework'),
    path('homework/delete/<int:pk>/', views.delete_homework, name='delete_homework'),

    #Youtube
    path('youtube/', views.youtube, name='youtube'),

    #todo app
    path('todo/', views.TodoApp, name='todo'),
    path('todo/update/<int:pk>/', views.update_todo, name='update_todo'),
    path('todo/delete/<int:pk>/', views.delete_todo, name='delete_todo'),

    #books app
    path('books/', views.books, name='books'),

    #Dictionary app
    path('dictionary/', views.Dictionary, name='dictionary'),

    #Wikipedia app
    path('wikipedia/', views.Wikipedia, name='wikipedia'),

    #Conversion app
    path('conversion/', views.Conversion, name='conversion'),
    
    
]
