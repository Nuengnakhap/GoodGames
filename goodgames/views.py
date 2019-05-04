from django.shortcuts import render, redirect

# Create your views here.
from goodgames.forms import RegistrationForm


def index(request):
    context = {
    }

    try:
        context['dayoff_list'] = None
        context['user'] = None
    except:
        context['dayoff_list'] = None

    return render(request, 'goodgames/index.html', context=context)


def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = RegistrationForm()

        context = {'form': form}

    return render(request, 'goodgames/register.html', context)