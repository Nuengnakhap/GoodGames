from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from goodgames.forms import RegistrationForm, UserAdminCreationForm
from django.contrib import messages

from goodgames.models import Tournament, Team


def index(request):
    return render(request, 'goodgames/index.html')


def register(request):
    form = RegistrationForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        print(form.data['email'])
        if form.is_valid():
            print('true')
            form.save()
            # return redirect('index')

    return render(request, 'goodgames/register.html', context)


def myLogin(request):
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
            context['success'] = 'Login Success'
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, 'goodgames/login.html', context)


def myLogout(request):
    logout(request)
    return redirect('index')


def tournament(request):
    context = {}
    query = '''
        SELECT t.id ,t.name as TournamentName, COUNT(team_id) as Team_Join, t.start_date, t.end_date, t.rule, t.prize, t.description, t.categories_id
        FROM goodgames_match m 
        JOIN goodgames_match_team mt 
        on mt.match_id = m.id 
        RIGHT OUTER JOIN goodgames_tournament t 
        on m.tournament_id = t.id 
        GROUP by t.id
    '''
    try:
        cmd = Tournament.objects.raw(query)
        context['tournament_list'] = cmd
        lst_prize = {}
        for i in cmd:
            # tmp_prize = ''
            # for j in range(i.prize.index('$'), i.prize.index('USD')+3):
            #     tmp_prize += i.prize[j]
            lst_prize[i.id] = i.prize.replace('\r', '').split('\n')
        context['prize'] = lst_prize

    except:
        context['tournament_list'] = None
    return render(request, 'goodgames/tournament.html', context)


def tournament_info(request, tour_id):
    context = {}
    query = '''
            SELECT t.id ,t.name as TournamentName, COUNT(team_id) as Team_Join, t.start_date, t.end_date, t.rule, t.prize, t.description, t.categories_id
            FROM goodgames_match m 
            JOIN goodgames_match_team mt 
            on mt.match_id = m.id 
            RIGHT OUTER JOIN goodgames_tournament t 
            on m.tournament_id = t.id 
            GROUP by t.id
            HAVING t.id = %d
        ''' % tour_id
    try:
        cmd = Tournament.objects.raw(query)
        context['tournament'] = cmd
        lst_prize = {}
        str_rule = ''
        for i in cmd:
            lst_prize[i.id] = i.prize.replace('\r', '').split('\n')
            str_rule = i.rule.replace('\r', '+').replace('\n', '+').split('+')
        context['prize'] = lst_prize
        context['rule'] = str_rule

    except:
        context['tournament'] = None
    return render(request, 'goodgames/tournamentinfo.html', context)


def team_info(request, team_id):
    context = {}
    winner = '''
            SELECT team.id, team.name as 'TeamName', COUNT(winner_id) as 'Wins'
            FROM goodgames_match m
            JOIN goodgames_tournament t
            on m.tournament_id = t.id
            JOIN goodgames_team team
            on winner_id = team.id
            GROUP by winner_id
            HAVING winner_id = %d
        ''' % team_id
    loser = '''
            SELECT team.id, team.name as 'TeamName', COUNT(loser_id) as 'Loses'
            FROM goodgames_match m
            JOIN goodgames_tournament t
            on m.tournament_id = t.id
            JOIN goodgames_team team
            on loser_id = team.id
            GROUP by loser_id
            HAVING loser_id = %d
        ''' % team_id

    try:
        cmd_win = Team.objects.raw(winner)
        cmd_lose = Team.objects.raw(loser)
        context['team'] = Team.objects.all().filter(id=team_id)
        context['win'] = cmd_win
        context['lose'] = cmd_lose
    except:
        context['win'] = None
        context['lose'] = None

    return render(request, 'goodgames/team.html', context)
