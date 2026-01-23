from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes, Homework
from .forms import *
from django.contrib import messages
from django.views import generic

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
    return redirect('note')


class NoteDetailView(generic.DetailView):
    model = Notes


def homework(request):
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