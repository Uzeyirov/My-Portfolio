from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, JoinRequest

def team_list(request):
    teams = Team.objects.all().order_by('-created_at')
    return render(request, 'teams/team_list.html', {'teams': teams})

# teams/views.py

# teams/views.py

@login_required
def create_team(request):
    if request.method == 'POST':
        # Şəkil gəldiyi üçün request.FILES mütləq olmalıdır
        name = request.POST.get('name')
        description = request.POST.get('description')
        looking_for = request.POST.get('looking_for')
        image = request.FILES.get('image') # Şəkli buradan tuturuq

        team = Team.objects.create(
            name=name,
            description=description,
            looking_for=looking_for,
            image=image, # Modeldə yaratdığımız sahəyə ötürürük
            leader=request.user
        )
        return redirect('team_list')
    
    return render(request, 'teams/create_team.html')

def team_list(request):
    teams = Team.objects.all().order_by('-created_at')
    return render(request, 'teams/team_list.html', {'teams': teams})



@login_required
def send_join_request(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        # Lider özünə müraciət edə bilməz
        if team.leader == request.user:
            return redirect('team_list')
            
        message_text = request.POST.get('message', '')

        # UNIQUE constraint xətası almamaq üçün update_or_create istifadə edirik
        # Bu metod: taparsa yeniləyir, tapmazsa yaradır.
        JoinRequest.objects.update_or_create(
            team=team, 
            user=request.user,
            defaults={
                'message': message_text,
                'status': 'pending'  # Yenidən müraciət edirsə statusu gözləməyə qaytarırıq
            }
        )
        
    return redirect('team_list')

@login_required
def manage_requests(request):
    # Lider olduğun komandalara gələn müraciətlər
    my_teams = Team.objects.filter(leader=request.user)
    incoming_requests = JoinRequest.objects.filter(team__in=my_teams, status='pending')
    return render(request, 'teams/manage_requests.html', {'requests': incoming_requests})


@login_required
def approve_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id, team__leader=request.user)
    join_request.status = 'accepted'
    join_request.save()
    # İstifadəçini komanda üzvlərinə əlavə edirik
    join_request.team.members.add(join_request.user)
    return redirect('manage_requests')

@login_required
def reject_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id, team__leader=request.user)
    join_request.status = 'rejected'
    join_request.save()
    return redirect('manage_requests')


# teams/views.py
@login_required
def approve_team_request(request, request_id):
    # JoinRequest modelində team sahəsinin olduğunu fərz edirik
    join_req = get_object_or_404(JoinRequest, id=request_id, team__creator=request.user)
    
    join_req.status = 'approved'
    join_req.save()
    
    # İstifadəçini komandaya rəsmən üzv edirik
    team = join_req.team
    team.members.add(join_req.user)
    
    return redirect('manage_requests')




from django.contrib import messages
@login_required
def team_workspace(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    # Yoxlayırıq: İstifadəçi liderdir, yoxsa üzv?
    is_leader = (request.user == team.leader)
    is_member = team.members.filter(id=request.user.id).exists()

    if is_leader or is_member:
        # ƏSAS HİSSƏ: Bu komandaya aid bütün mesajları bazadan gətiririk
        chat_messages = team.messages.all().order_by('timestamp')
        
        return render(request, 'teams/team_workspace.html', {
            'team': team,
            'chat_messages': chat_messages  # <-- Mesajları bura əlavə etdik
        })
    else:
        messages.error(request, "Siz bu komandanın üzvü deyilsiniz!")
        return redirect('team_list')
    


from django.http import JsonResponse
from .models import Team, TeamMessage # TeamMessage-i bura əlavə etdik

@login_required
def send_message(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, id=team_id)

        # Təhlükəsizlik: Yalnız üzvlər mesaj yaza bilsin
        if request.user == team.leader or request.user in team.members.all():
            content = request.POST.get('content')
            image = request.FILES.get('image')
            file = request.FILES.get('file')

            msg = TeamMessage.objects.create(
                team=team,
                user=request.user,
                content=content,
                image=image,
                file=file
            )

            return JsonResponse({
                'status': 'success',
                'user': msg.user.username,
                'content': msg.content,
                'image_url': msg.image.url if msg.image else None,
                'file_url': msg.file.url if msg.file else None,
                'file_name': msg.file.name.split('/')[-1] if msg.file else None,
                'timestamp': msg.timestamp.strftime('%H:%M')
            })
            
    return JsonResponse({'status': 'error'}, status=400)


# teams/views.py

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'teams/team_detail.html', {'team': team})



# teams/views.py
from django.contrib.auth.models import User
@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user in team.members.all() and request.user != team.leader:
        team.members.remove(request.user)
        messages.success(request, f"{team.name} komandasından çıxdınız.")
    elif request.user == team.leader:
        messages.error(request, "Lider komandanı tərk edə bilməz! Əvvəlcə liderliyi təhvil verməli və ya komandanı silməlisiniz.")
    return redirect('team_list')

from django.contrib.auth import get_user_model

User = get_user_model() # Bu, hal-hazırda aktiv olan User modelini avtomatik tapır

@login_required
def remove_member(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    # User modelini yuxarıdakı kimi təyin etdikdən sonra:
    user_to_remove = get_object_or_404(User, id=user_id)
    
    if request.user == team.leader and user_to_remove != team.leader:
        team.members.remove(user_to_remove)
        
    return redirect('team_workspace', team_id=team.id)