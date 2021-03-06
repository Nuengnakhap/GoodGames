import json
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import render, redirect
# Create your views here.
from django.utils import timezone

from goodgames.components import power_of_two
from goodgames.forms import RegistrationForm, CreateTeamForm, ManageTeamForm, ManagePlayerForm, \
    NoticeForm, CreateTournamentForm, ManageTournamentForm
from goodgames.models import Tournament, Team, Match, Player, Organizer, Categories


def error404(request):
    return render(request, 'goodgames/404.html', status=404)


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
            # return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, 'goodgames/login.html', context)


@login_required
def myLogout(request):
    logout(request)
    return redirect('index')


@login_required
def manage_player(request):
    context = {}
    current_user = request.user
    if request.method == 'POST':
        form = ManagePlayerForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            context['success'] = 'Edited Your Information!'
            # return redirect('manage_player')
        else:
            context['error'] = 'Cannot Edit Your Information!'
    else:
        form = ManagePlayerForm(instance=current_user)
    context['form'] = form

    return render(request, 'goodgames/manageplayer.html', context)


# -------------------------- TOURNAMENT VIEWS -------------------------- #
@login_required
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
    owner = Organizer.objects.filter(username=request.user)
    if owner.exists():
        context['owner'] = True
    else:
        context['owner'] = False
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


@login_required
def tournament_info(request, tour_id):
    current_user = request.user
    context = {}
    # query = '''
    #         SELECT t.id ,t.name as TournamentName, COUNT(team_id) as Team_Join, t.start_date, t.end_date, t.rule, t.prize, t.description, t.categories_id
    #         FROM goodgames_match m
    #         JOIN goodgames_match_team mt
    #         on mt.match_id = m.id
    #         RIGHT OUTER JOIN goodgames_tournament t
    #         on m.tournament_id = t.id
    #         GROUP by t.id
    #         HAVING t.id = %d
    #     ''' % tour_id

    tournament = Tournament.objects.filter(id=tour_id).values('id', 'name', 'start_date', 'end_date', 'rule', 'prize', 'description', 'categories').annotate(team_join=Count('match__team'))

    tournament = [{'id': x['id'], 'TournamentName': x['name'], 'start_date': x['start_date'], 'end_date': x['end_date'], 'rule': x['rule'], 'prize': x['prize'], 'description': x['description'], 'categories': x['categories'], 'team_join': x['team_join']} for x in tournament]

    tour = Tournament.objects.get(id=tour_id)
    user = current_user

    team = Team.objects.filter(player_create=user)
    owner = Organizer.objects.filter(username=current_user)
    match = Tournament.objects.filter(team_join__in=team, team_join__player_create=user).values('team_join__name')

    if match.exists():
        context['joined'] = True
    else:
        context['joined'] = False
    if team.exists():
        context['can_join'] = True
    else:
        context['can_join'] = False
    if owner.exists():
        context['owner'] = True
    else:
        context['owner'] = False

    if request.method == 'POST':
        for i in team:
            tour.team_join.add(i)

    try:
        # cmd = Tournament.objects.raw(query)
        context['tournament'] = tournament
        lst_prize = {}
        str_rule = ''
        for i in tournament:
            lst_prize[i['id']] = i['prize'].replace('\r', '').split('\n')
            str_rule = i['rule'].replace('\r', '+').replace('\n', '+').split('+')
        context['prize'] = lst_prize
        context['rule'] = str_rule

    except:
        context['tournament'] = None
    return render(request, 'goodgames/tournamentinfo.html', context)


@login_required
def tournament_bracket(request, tour_id):
    current_user = request.user
    context = {}

    match = Match.objects.filter(tournament_id=tour_id)
    owner = Organizer.objects.filter(username=current_user).distinct()

    if match.exists():
        context['built'] = True
        mt = match.values('team__matchs__team__name').distinct()
        match = [{'team': x['team__matchs__team__name']} for x in mt]
        tmp = []
        teams = []
        for i in range(len(match)):
            tmp.append(match[i]['team'])

        team = Tournament.objects.filter(id=tour_id).values('team_join__name')

        for i in range(0, len(tmp) - 1, 2):
            teams.append([tmp[i], tmp[i + 1]])

        # print(teams)

        if team.count() != mt.count():
            team = [{'team': x['team_join__name']} for x in team]

            team_all = []
            for i in range(len(team)):
                team_all.append(team[i]['team'])

            num_team = power_of_two(len(team_all) // 2)

            for i in range(len(team)):
                if team_all[i] not in tmp:
                    teams.append([team_all[i], None])

            if num_team > (len(team_all) // 2):
                for i in range((len(team_all) + 1) // 2, num_team):
                    teams.append([None, None])

            if len(team_all) % 2 != 0:
                num_team = power_of_two((len(team_all) + 1) // 2)

            if num_team > (len(team_all) // 2):
                for i in range((len(team_all) + 1) // 2, num_team):
                    teams.append([None, None])

            # print(teams)
        data = {'teams': teams, 'results': []}
        context['data'] = json.dumps(data)

    else:
        context['built'] = False
        team = Tournament.objects.filter(id=tour_id).values('team_join__name')
        team = [{'team': x['team_join__name']} for x in team]
        team_all = []
        teams = []

        for i in range(len(team)):
            team_all.append(team[i]['team'])
        random.shuffle(team_all)

        num_team = power_of_two(len(team_all) // 2)

        for i in range(0, len(team_all) - 1, 2):
            teams.append([team_all[i], team_all[i + 1]])

        if len(team_all) % 2 != 0:
            teams.append([team_all[len(team_all) - 1], None])
            num_team = power_of_two((len(team_all) + 1) // 2)

        if num_team > (len(team_all) // 2):
            for i in range((len(team_all) + 1) // 2, num_team):
                teams.append([None, None])

        data = {'teams': teams, 'results': []}
        context['data'] = json.dumps(data)

    if request.method == 'POST':
        count = 0
        iterpost = iter(request.POST)
        next(iterpost)
        team = []
        tmp = []
        for key in iterpost:
            value = request.POST[key]
            tmp.append(value)
            count += 1
            if count % 2 == 0 and count != 0:
                match = Match(start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=7),
                              tournament_id=tour_id)
                match.save()
                t1 = Team.objects.get(name=tmp[0])
                t2 = Team.objects.get(name=tmp[1])
                match.team.add(t1.id, t2.id)
                team.append(tmp)
                tmp = []
        return redirect('tournament_info', tour_id)

    if owner.exists():
        return render(request, 'goodgames/tournamentbracket.html', context)
    else:
        return redirect('error')


@login_required
def create_tournament(request):
    current_user = request.user
    organizer = Organizer.objects.filter(username=current_user).distinct()
    if request.method == 'POST':
        form = CreateTournamentForm(request.POST)
        if form.is_valid():
            form.save()

            tournament = Tournament.objects.get(name=form.cleaned_data['name'])
            tournament.organizer = organizer
            tournament.save()
            return redirect('tournament_info', tournament.id)
        else:
            Categories.objects.create(description=form.data['new_type'])
    else:
        form = CreateTournamentForm()
    context = {'form': form}
    if organizer.exists():
        return render(request, 'goodgames/createtournament.html', context)
    else:
        return redirect('error')


@login_required
def manage_tournament(request, tour_id):
    context = {}
    current_user = request.user
    tour = Tournament.objects.get(id=tour_id)
    context['tour_id'] = tour_id
    context['error'] = ''
    if request.method == 'POST':
        form = ManageTournamentForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            context['success'] = 'Edited Your Information!'
            # return redirect('manage_player')
        else:
            Categories.objects.create(description=form.data['new_type'])
            form = ManageTournamentForm(instance=tour)
    else:
        form = ManageTournamentForm(instance=tour)
    context['form'] = form

    if tour.organizer.username == current_user:
        return render(request, 'goodgames/managetournament.html', context)
    else:
        return redirect('error')


# -------------------------- TEAM VIEWS -------------------------- #
def team(request):
    context = {}

    try:
        cmd = Team.objects.all()
        context['teams'] = cmd

    except:
        context['teams'] = None
    return render(request, 'goodgames/allteam.html', context)


@login_required
def team_info(request, team_id):
    context = {}
    current_user = request.user
    team = Team.objects.get(id=team_id)
    if request.method == 'POST' and current_user.id != None:
        team.player_join.add(current_user)

    # winner = '''
    #         SELECT team.id, team.name as 'TeamName', COUNT(winner_id) as 'Wins'
    #         FROM goodgames_match m
    #         JOIN goodgames_tournament t
    #         on m.tournament_id = t.id
    #         JOIN goodgames_team team
    #         on winner_id = team.id
    #         GROUP by winner_id
    #         HAVING winner_id = %d
    #     ''' % team_id
    # loser = '''
    #         SELECT team.id, team.name as 'TeamName', COUNT(loser_id) as 'Loses'
    #         FROM goodgames_match m
    #         JOIN goodgames_tournament t
    #         on m.tournament_id = t.id
    #         JOIN goodgames_team team
    #         on loser_id = team.id
    #         GROUP by loser_id
    #         HAVING loser_id = %d
    #     ''' % team_id
    # match = Match.objects.filter(winner=team).values('winner__name', 'winner').annotate(num=Count('winner'))
    winner = Match.objects.filter(winner=team)
    loser = Match.objects.filter(loser=team)

    try:
        # cmd_win = Team.objects.raw(winner)
        # cmd_lose = Team.objects.raw(loser)
        context['team'] = Team.objects.all().filter(id=team_id)
        context['win'] = winner
        context['lose'] = loser
        if team.player_create == current_user:
            context['owner'] = True

    except:
        context['team'] = None
        context['win'] = None
        context['lose'] = None
        context['owner'] = False

    return render(request, 'goodgames/team.html', context)


@login_required
def match_team(request, team_id):
    context = {}
    current_user = request.user
    team = Team.objects.get(id=team_id)

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
        if team.player_create == current_user:
            context['owner'] = True
    except:
        context['matchs'] = None
        context['owner'] = False

    if team.player_create == current_user:
        return render(request, 'goodgames/match.html', context)
    else:
        return redirect('error')


@login_required
def create_team(request):
    current_user = request.user
    player = Player.objects.get(id=current_user.id)
    owner = Group.objects.get(name='team_owner')
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            team = Team.objects.get(name=form.data['name'])
            team.player_create = player
            team.save()
            owner.user_set.add(player)
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


@login_required
def manage_team(request, team_id):
    context = {}
    team_info = Team.objects.get(id=team_id)
    player_join = team_info.player_join.all()
    player_team = team_info.player_team.all()
    if request.method == 'POST':
        if request.FILES:
            form = ManageTeamForm(request.POST, request.FILES, instance=team_info)
            if form.is_valid():
                form.save()
                return redirect('team_info', team_id)
        else:
            form = ManageTeamForm(instance=team_info)
            iterpost = iter(request.POST)
            next(iterpost)
            for key in iterpost:
                value = request.POST[key]
                player = Player.objects.get(username=value)
                if 'delete-' in key:
                    team_info.player_join.remove(player)
                elif 'del-team-' in key:
                    team_info.player_team.remove(player)
                else:
                    team_info.player_team.add(player)
                    team_info.player_join.remove(player)
            return redirect('team_info', team_id)


    else:
        form = ManageTeamForm(instance=team_info)

        try:
            context['players_team'] = player_team
            context['players_join'] = player_join
        except:
            context['players_team'] = None
            context['players_join'] = None

    context['form'] = form

    if team_info.player_create == request.user:
        return render(request, 'goodgames/ManageTeamInfo.html', context)
    else:
        return redirect('error')


# -------------------------- OTHER VIEWS -------------------------- #
def ranking(request):
    context = {}

    # query = '''
    #     SELECT team.id, t.name as 'TournamentName', team.name as 'TeamName', COUNT(winner_id) as 'Wins'
    #     from goodgames_match m
    #     JOIN goodgames_tournament t
    #     on m.tournament_id = t.id
    #     JOIN goodgames_team team
    #     on winner_id = team.id
    #     GROUP by tournament_id, winner_id
    #     '''
    ranks = Match.objects.values('tournament__name', 'winner__name').annotate(wins=Count('winner')).order_by('-tournament__created_at', '-wins')

    if ranks[0]['winner__name'] == None:
        context['ranks'] = None
        context['tournaments'] = None
    else:
        context['tournaments'] = Tournament.objects.filter(name__in=[f['tournament__name'] for f in ranks])
        context['ranks'] = ranks

    # try:
    #     # rank = Tournament.objects.raw(query)
    #     context['tournaments'] = Tournament.objects.filter(name__in=[f['tournament__name'] for f in ranks])
    #     context['ranks'] = ranks
    # except:
    #     context['ranks'] = None
    #     context['tournaments'] = None
    return render(request, 'goodgames/ranking.html', context)


@login_required
def notice_result(request, team_id, match_id):
    context = {}
    match = Match.objects.get(pk=match_id)
    home = ''
    away = ''
    for team in match.team.all():
        if team.id == team_id:
            home = team
        else:
            away = team

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=match)

        if form.is_valid():
            if request.POST.get('result') == 'win':
                match.winner = home
                match.loser = away
                match.save()
            else:
                match.winner = away
                match.loser = home
                match.save()
            form.save()
            return redirect('match_team', team_id)
    else:
        form = NoticeForm(instance=match)

    try:
        context['form'] = form
        context['match_id'] = match_id
        context['match'] = match.get_teams()
    except:
        context['form'] = None
        context['match_id'] = None
        context['match'] = None

    team = Team.objects.get(id=team_id)
    if team.player_create == request.user:
        return render(request, 'goodgames/noticeresult.html', context)
    else:
        return redirect('error')
