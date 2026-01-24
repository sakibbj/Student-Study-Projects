from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes, Homework, Todo
from .forms import *
from django.contrib import messages
from django.views import generic
from youtube_search import YoutubeSearch

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Notes Added Successfully by {request.user.username}!")
            return redirect('note')
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {
        "notes": notes,
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    notes = get_object_or_404(Notes, pk=pk)
    notes.delete()
    messages.warning(request, f"Note Deleted by {request.user.username}!")
    return redirect('note')


class NoteDetailView(generic.DetailView):
    model = Notes


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subjects = request.POST['subjects'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, f"Homework Added form {request.user.username}!")
            return redirect('homework')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
        "homework": homework,
        "homework_done": homework_done,
        "form": form,
    }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk):
    if request.method == 'POST':
        homework = get_object_or_404(Homework, pk=pk)
        homework.is_finished = not homework.is_finished
        homework.save()
    return redirect('homework')


def delete_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    homework.delete()
    messages.warning(request, f"Homework Deleted by {request.user.username}!")
    return redirect('homework')


def youtube(request):
    result_list = []

    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            videos = YoutubeSearch(text, max_results=10).to_dict()
            
            for video in videos:
                result_list.append({
                    'title': video.get('title', ''),
                    'duration': video.get('duration', ''),
                    'thumbnail': video.get('thumbnails', [''])[0],
                    'channel': video.get('channel', ''),
                    'link': 'https://www.youtube.com' + video.get('url_suffix', ''),
                    'views': video.get('views', ''),
                })

    else:
        form = DashboardForm()
    context = {
        'form': form,
        'results': result_list
    }
    return render(request, 'dashboard/youtube.html', context)

def TodoApp(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, f"Title Added Successfully by {request.user.username}!")
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todo': todo,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/todo.html', context)

def update_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        todo.is_finished = not todo.is_finished
        todo.save()
        return redirect('todo')
    

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.warning(request, f"Title Deleted by {request.user.username}!")
    return redirect('todo')


