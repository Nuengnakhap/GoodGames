import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from polls.models import Poll, Question, Answer, Choice
from .forms import PollModelForm, QuestionForm, CommentForm, CreateQuestion, QuestionModelForm, \
    ChoiceModelForm


# Create your views here.
def index(request):
    poll_list = Poll.objects.all()

    for poll in poll_list:
        question_count = Question.objects.filter(poll_id=poll.id).count()
        poll.question_count = question_count

    context = {
        'page_title': "My Polls",
        'poll_list': poll_list
    }
    return render(request, template_name='polls/index.html', context=context)


@login_required
@permission_required('polls.view_poll')
def detail(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    for question in poll.question_set.all():
        name = 'choice' + str(question.id)
        choice_id = request.GET.get(name)
        if choice_id:
            try:
                ans = Answer.objects.get(question_id=question.id)
                ans.choice_id = choice_id
            except Answer.DoesNotExist:
                Answer.objects.create(
                    choice_id=choice_id,
                    question_id=question.id
                )

    return render(request, 'polls/detail.html', {'poll': poll})


# Poll CRUD Function #

def create_poll(request):
    context = {}
    ques = 0
    QuestionFormSet = formset_factory(QuestionForm, extra=2)
    if request.method == 'POST':
        form = PollModelForm(request.POST)

        formset = QuestionFormSet(request.POST)
        if form.is_valid():
            poll = form.save()
            if formset.is_valid():
                for question_form in formset:
                    Question.objects.create(
                        text=question_form.cleaned_data.get('text'),
                        type=question_form.cleaned_data.get('type'),
                        poll_id=poll.id
                    )
                    # ques += 1
                context['success'] = "Poll %s is created successfully!" % poll.title
                # ques = 0
            # poll = Poll.objects.create(
            #     title=form.cleaned_data.get('title'),
            #     start_date=form.cleaned_data.get('start_date'),
            #     end_date=form.cleaned_data.get('end_date'),

            # )
            # for i in range(1, form.cleaned_data.get('no_questions')+1):
            #     Question.objects.create(
            #         text='QQQQ'+str(i),
            #         type='01',
            #         poll=poll
            #     )
    else:
        form = PollModelForm()
        formset = QuestionFormSet()

    context['form'] = form
    context['formset'] = formset

    return render(request, 'polls/create_poll.html', context=context)


@login_required
def update_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    QuestionFormSet = formset_factory(QuestionForm, extra=2)
    context = {'poll': poll}

    if request.method == 'POST':
        form = PollModelForm(request.POST)
        formset = QuestionFormSet(request.POST)

        if form.is_valid():
            # form.save()
            if formset.is_valid():
                for question_form in formset:
                    if question_form.cleaned_data.get('question_id'):
                        question = Question.objects.get(id=question_form.cleaned_data.get('question_id'))

                        if question:
                            question.text = question_form.cleaned_data.get('text')
                            question.type = question_form.cleaned_data.get('type')
                            question.save()
                    else:
                        if question_form.cleaned_data.get('text'):
                            Question.objects.create(
                                text=question_form.cleaned_data.get('text'),
                                type=question_form.cleaned_data.get('type'),
                                poll_id=poll.id
                            )
            context['success'] = "Saved successful"
            formset = QuestionFormSet(initial=[{'text': i.text, 'type': i.type, 'question_id': i.id}
                                               for i in poll.question_set.all()])

    else:
        form = PollModelForm(instance=poll)
        data = []
        for question in poll.question_set.all():
            data.append(
                {
                    'text': question.text,
                    'type': question.type,
                    'question_id': question.id
                }
            )
        formset = QuestionFormSet(initial=data)

    context['form'] = form
    context['formset'] = formset

    return render(request, 'polls/update.html', context=context)


@login_required
def delete_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    context = {'poll': poll}
    if request.method == 'POST':
        # choices.delete()
        for q in poll.question_set.all():
            for c in q.choice_set.all():
                c.delete()
            q.delete()

        poll.delete()
        return redirect('index')
    else:
        return render(request, 'polls/delete_poll.html', context=context)


# Question CRUD Function #

@login_required
# CreateQuestion
def create_question(request, poll_id):
    context = {}
    ques = 0
    CreateQuestionFormSet = formset_factory(CreateQuestion, extra=2)
    if request.method == 'POST':
        form = QuestionModelForm(request.POST)

        formset = CreateQuestionFormSet(request.POST)
        if form.is_valid():
            poll = form.save()
            if formset.is_valid():
                for question_form in formset:
                    Question.objects.create(
                        text=question_form.cleaned_data.get('question'),
                        type=question_form.cleaned_data.get('type'),
                        poll_id=poll.id
                    )
                    Choice.objects.create(
                        text=question_form.cleaned_data.get('text'),
                        value=question_form.cleaned_data.get('value')
                    )
                    ques += 1
                context['success'] = "Poll %s is created successfully!" % poll.title
                ques = 0
            # poll = Poll.objects.create(
            #     title=form.cleaned_data.get('title'),
            #     start_date=form.cleaned_data.get('start_date'),
            #     end_date=form.cleaned_data.get('end_date'),

            # )
            # for i in range(1, form.cleaned_data.get('no_questions')+1):
            #     Question.objects.create(
            #         text='QQQQ'+str(i),
            #         type='01',
            #         poll=poll
            #     )
    else:
        form = QuestionModelForm()
        formset = CreateQuestionFormSet()

    context['form'] = form
    context['formset'] = formset

    return render(request, 'questions/create.html', context=context)


@login_required
def delete_question(request, poll_id, question_id):
    question = Question.objects.get(id=question_id)
    for i in question.choice_set.all():
        i.delete()
    question.delete()
    return redirect('update_poll', poll_id=poll_id)

# Choice CRUD Function #
@login_required
def add_choice(request, poll_id, question_id):
    poll = Poll.objects.get(id=poll_id)
    question = Question.objects.get(id=question_id)
    choices = [{'id': i.id, 'text': i.text, 'value': i.value, 'question': i.question_id}
               for i in question.choice_set.all()]
    context = {'poll': poll, 'question': question, 'choices': json.dumps(choices)}
    return render(request, 'choices/add.html', context=context)


@login_required
def add_choice_api(request, poll_id, question_id):
    if request.method == 'POST':
        choice_list = json.loads(request.body)
        error_message = None

        # Algorithm: Delete choices
        database_choice_list_ids = [i.id for i in Question.objects.get(pk=question_id).choice_set.all()]
        choice_list_ids = list()

        for i in choice_list:
            try:
                choice_list_ids.append(i['id'])
            except KeyError:
                pass

        for i in database_choice_list_ids:
            if i not in choice_list_ids:
                Choice.objects.get(pk=i).delete()

        # Algorithm: Validations
        for i in choice_list:
            if i['text'] == '' or i['value'] == '':
                error_message = 'Fields can\'t be left blank.'
                break
            error_message = None

        # Algorithm: Save choices
        if not error_message:
            for i in choice_list:
                try:
                    # Case: Choice already exists.
                    Choice.objects.filter(pk=i['id']).update(text=i['text'], value=i['value'])
                except KeyError:
                    # Case: Choice doesn't exist.
                    form = ChoiceModelForm({
                        'text': i['text'],
                        'value': i['value'],
                        'question': question_id
                    })
                    if form.is_valid():
                        form.save()
                    else:
                        error_message = 'Fields can\'t be left blank.'
                        break

        if not error_message:
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': error_message}, status=400)
    return JsonResponse({'message': 'This API does not accept GET request.'}, status=405)


@login_required
@permission_required('polls.add_comment')
def comment(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.save()
    else:
        form = CommentForm()

    context = {
        'form': form,
        'poll': poll
    }

    return render(request, 'polls/comment.html', context=context)


def mylogin(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')

            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, 'polls/login.html', context=context)


def mylogout(request):
    logout(request)
    return redirect('index')
