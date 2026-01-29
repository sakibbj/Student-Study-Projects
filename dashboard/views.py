from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes, Homework, Todo
from .forms import *
from django.contrib import messages
from django.views import generic
import requests, wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')
@login_required
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

@login_required
def delete_note(request, pk=None):
    notes = get_object_or_404(Notes, pk=pk)
    notes.delete()
    messages.warning(request, f"Note Deleted by {request.user.username}!")
    return redirect('note')


class NoteDetailView(generic.DetailView):
    model = Notes

@login_required
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

@login_required
def update_homework(request, pk):
    if request.method == 'POST':
        homework = get_object_or_404(Homework, pk=pk)
        homework.is_finished = not homework.is_finished
        homework.save()
    return redirect('homework')

@login_required
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
            youtube_api = build( 'youtube', 'v3',
                developerKey='AIzaSyB4zq6X5RsmlV704ettyBOZ8F0VVIR2ufE')

            response = youtube_api.search().list(
                q=text,
                part = 'snippet',
                type = 'video',
                maxResults = 10
            ).execute()

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']

                result_list.append({
                    'title': snippet.get('title', ''),
                    'thumbnail': snippet["thumbnails"]["medium"]["url"],
                    'channel': snippet.get('channelTitle', ''),
                    'link': f"https://www.youtube.com/watch?v={video_id}",
                    'duration': 'N/A',
                    'views': 'N/A',
                    'published': snippet.get('publishedAt', ''),
                    'description': snippet.get('description', ''),
                })

    else:
        form = DashboardForm()
    context = {
        'form': form,
        'results': result_list
    }
    return render(request, 'dashboard/youtube.html', context)
@login_required
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
@login_required
def update_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        todo.is_finished = not todo.is_finished
        todo.save()
        return redirect('todo')

@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.warning(request, f"Title Deleted by {request.user.username}!")
    return redirect('todo')


def books(request):
    results = []
    error = None

    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            url = f"https://www.googleapis.com/books/v1/volumes?q={text}&key=YOUR_API_KEY"
            r = requests.get(url)
            answer = r.json()

            if 'error' in answer:
                error = "For Today Google Books API quota Ends."
            else:
                for item in answer.get('items', [])[:10]:
                    volume = item.get('volumeInfo', {})
                    results.append({
                        'title': volume.get('title'),
                        'subtitle': volume.get('subtitle'),
                        'description': volume.get('description'),
                        'count': volume.get('pageCount'),
                        'categories': volume.get('categories'),
                        'rating': volume.get('averageRating'),
                        'thumbnail': volume.get('imageLinks', {}).get('thumbnail'),
                        'preview': volume.get('previewLink'),
                    })

    else:
        form = DashboardForm()

    return render(request, 'dashboard/books.html', {
        'form': form,
        'results': results,
        'error': error,
    })

def Dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text')

        if text:
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
            r = requests.get(url)
            answer = r.json()

            try:
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0]['definitions'][0]['example']
                synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms,
                }

            except Exception:
                context = {
                    'form': form,
                    'input': text,
                    'error': 'Word not found'
                }
        else:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)

    form = DashboardForm()
    return render(request, 'dashboard/dictionary.html', {'form': form})

def Wikipedia(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary,
            }
        except DisambiguationError as e:
            context = {
                'form': form,
                'error': "What Do You Mean?",
                'options': e.options[:10]
            }

        except PageError:
            context = {
                'form': form,
                'error': "Nothing Found"
            }
        return render(request, 'dashboard/wikipedia.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/wikipedia.html', context)



def Conversion(request):

    context = {
        'form': ConversionForm(),
        'input': False,
        'm_form': None,
        'answer': ''
    }
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        context['form'] = form
        context['input'] = True

        if form.is_valid():
            measurement = form.cleaned_data['measurement']
            if measurement == 'length':
                m_form = ConversionLengthForm(request.POST)
            else:
                m_form = ConversionMassForm(request.POST)

            context['m_form'] = m_form

            if m_form.is_valid():
                value = m_form.cleaned_data['value']
                first = m_form.cleaned_data['measure1']
                second = m_form.cleaned_data['measure2']

                if value is not None and value >= 0:
                    if measurement == 'length':
                        if first == 'yard' and second == 'foot':
                            context['answer'] = f"{value} yard = { value * 3} foot"
                        elif first == 'foot' and second == 'yard':
                            context['answer'] = f"{value} foot = { value / 3} yard"
                        else:
                            context['answer'] = "Same unit Selected"

                    elif measurement == 'mass':
                        if first == 'pound' and second == 'kilogram':
                            context['answer'] = f"{value} pound = { value * 0.453592} kilogram"
                        elif first == 'kilogram' and second == 'pound':
                            context['answer'] = f"{value} kilogram = { value * 2.20462} pound"
                        else:
                            context['answer'] = "Same unit Selected"

    return render(request, 'dashboard/conversion.html', context)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Welcome {username}! Your Account was created Successfully.")
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/profile.html', context)