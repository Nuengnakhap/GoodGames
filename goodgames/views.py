from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from goodgames.forms import RegistrationForm, UserAdminCreationForm, CreateTeamForm
from django.contrib import messages

from goodgames.models import Tournament, Team, Match


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
            return redirect('login')

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


def match_team(request, team_id):
    context = {}
    query = '''
            SELECT j.id, c.description as type, tm.name as tour_name, t.team_id as my_team_id, 
            g.name as my_team, m.team_id as enemy_team_id, k.name as enemy_team, 
            j.winner_id, j.loser_id, j.start_date, j.end_date
            FROM goodgames_match_team t
            JOIN goodgames_match_team m
            ON t.match_id = m.match_id
            JOIN goodgames_match j
            ON j.id = t.match_id
            JOIN goodgames_team g
            ON g.id = t.team_id
            JOIN goodgames_team k
            ON k.id = m.team_id
            JOIN goodgames_tournament tm
            ON tm.id = j.tournament_id
            JOIN goodgames_categories c
            ON c.id = tm.categories_id
            WHERE t.team_id != m.team_id
            AND t.team_id = %d
            ''' % team_id
    try:
        context['matchs'] = Match.objects.raw(query)
    except:
        context['matchs'] = None
    return render(request, 'goodgames/match.html', context)


def create_team(request):

    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            team = Team.objects.get(name=form.data['name'])
            return redirect('team_info', team.id)
    else:
        form = CreateTeamForm()
    context = {'form': form}
    return render(request, 'goodgames/createteam.html', context)

def team(request):
    context = {}
    try:
        cmd = Team.objects.all()
        context['teams'] = cmd

    except:
        context['teams'] = None
    return render(request, 'goodgames/allteam.html', context)

def ranking(request):
    context = {}

    query = '''
        SELECT team.id, t.name as 'TournamentName', team.name as 'TeamName', COUNT(winner_id) as 'Wins'
        from goodgames_match m 
        JOIN goodgames_tournament t
        on m.tournament_id = t.id 
        JOIN goodgames_team team 
        on winner_id = team.id 
        GROUP by tournament_id, winner_id
        '''
    try:
        rank = Tournament.objects.raw(query)
        context['tournaments'] = Tournament.objects.filter(name__in=[f.TournamentName for f in rank])
        context['ranks'] = rank
    except:
        context['ranks'] = None
        context['tournaments'] = None
    return render(request, 'goodgames/ranking.html', context)