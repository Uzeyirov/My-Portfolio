from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IdeaForm
from .models import Idea

def home(request):
    # Bütün ideyaları çəkib ana səhifəyə (home.html) göndəririk
    ideas = Idea.objects.all()
    context = {
        'ideas': ideas,
        'title': 'Ana Səhifə - İdeyalar'
    }
    return render(request, 'innovation/home.html', context)


# Ana səhifə funksiyan artıq ordadır, onun altına bunu əlavə et:

@login_required
def create_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES) # Şəkil üçün request.FILES vacibdir
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user # İdeyanı paylaşan hazırkı istifadəçidir
            idea.save()
            return redirect('home')
    else:
        form = IdeaForm()
    return render(request, 'innovation/create_idea.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Idea

@login_required
def vote_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    # Əgər istifadəçi artıq səs veribsə, səsini geri çəkirik
    if idea.votes.filter(id=request.user.id).exists():
        idea.votes.remove(request.user)
    else:
        # Əgər səs verməyibsə, səsini əlavə edirik
        idea.votes.add(request.user)
    
    referer = request.META.get('HTTP_REFERER')
    
    if referer:
        # Əgər artıq URL-də köhnə bir #id varsa, onu təmizləyirik
        base_url = referer.split('#')[0]
        # İstifadəçini birbaşa həmin ideyanın olduğu hissəyə göndəririk
        return redirect(f"{base_url}#idea-{idea.id}")
    
    return redirect('home')

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'innovation/idea_detail.html', {'idea': idea})



from .forms import IdeaForm, CommentForm # CommentForm əlavə et
from .models import Idea, Comment # Comment modelini də əlavə et

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    # Səhifədə ancaq ana rəyləri (parent=None olanları) əsas siyahıda göstəririk
    comments = idea.comments.filter(parent=None)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            
            # Əgər cavab formundan parent_id gəlibsə, onu mənimsədirik
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
                
            comment.save()
            return redirect(f"{request.path}#comment-{comment.id}")
    else:
        form = CommentForm()

    return render(request, 'innovation/idea_detail.html', {
        'idea': idea,
        'comments': comments,
        'comment_form': form
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Idea, Profile
from .forms import UserUpdateForm, ProfileUpdateForm

def profile_view(request, username=None):
    # Əgər URL-də username varsa, həmin adamı tap, yoxdursa daxil olan istifadəçini götür
    if username:
        user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user

    # Profil yoxdursa yaradırıq (təhlükəsizlik üçün)
    profile, created = Profile.objects.get_or_create(user=user)

    # Redaktə formaları (ancaq öz profilindəsənsə görüksün)
    u_form = None
    p_form = None
    if request.user == user:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('profile', username=user.username)
        else:
            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=profile)

    # Statistika və ideyalar (tapılan istifadəçiyə görə)
    my_ideas = Idea.objects.filter(author=user)
    voted_ideas = user.idea_votes.all()
    total_votes_received = sum(idea.total_votes() for idea in my_ideas)

    return render(request, 'innovation/profile.html', {
        'profile_user': user, # Şablonda 'user' yox, 'profile_user' istifadə edəcəyik
        'u_form': u_form,
        'p_form': p_form,
        'my_ideas': my_ideas,
        'voted_ideas': voted_ideas,
        'total_votes_received': total_votes_received,
    })

from django.contrib.auth import get_user_model

User = get_user_model() # Bu sətir aktiv User modelini dinamik şəkildə götürür



from django.contrib import messages

# İDEYANI REDAKTƏ ETMƏK
@login_required
def edit_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if idea.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        # 'instance=idea' mütləq olmalıdır ki, yeni post yaratmasın, mövcudu yeniləsin
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    
    return render(request, 'innovation/create_idea.html', {
        'form': form,
        'title': 'İdeyanı Redaktə Et'
    })

# İDEYANI SİLMƏK
@login_required
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if idea.author != request.user:
        messages.error(request, "Siz ancaq öz ideyanızı silə bilərsiniz!")
        return redirect('idea_detail', pk=pk)
    
    if request.method == 'POST':
        idea.delete()
        messages.success(request, "İdeya uğurla silindi!")
        return redirect('profile', username=request.user.username)
    
    return render(request, 'innovation/idea_confirm_delete.html', {'idea': idea})



@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    idea_id = comment.idea.id # Silindikdən sonra geri qayıtmaq üçün ideyanın ID-si

    # Təhlükəsizlik: Rəyi ancaq sahibi silə bilər
    if comment.author == request.user:
        comment.delete()
        messages.success(request, "Rəyiniz silindi.")
    else:
        messages.error(request, "Siz bu rəyi silə bilməzsiniz!")
    
    return redirect('idea_detail', pk=idea_id)


# innovation/views.py

from django.db.models import Q

# views.py daxilində home funksiyasını belə yenilə:
def home(request):
    query = request.GET.get('q')
    if query:
        # icontains -> case-insensitive (hərf həssaslığı olmadan) axtarır
        ideas = Idea.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query) # Kateqoriyaya görə də axtaraq
        ).distinct().order_by('-created_at')
    else:
        ideas = Idea.objects.all().order_by('-created_at')

    context = {
        'ideas': ideas,
        'search_query': query # Yazılan sözü geri göndəririk ki, input-da qalsın
    }
    return render(request, 'innovation/home.html', context)



from .models import Solution

@login_required
def add_solution(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        
        Solution.objects.create(
            idea=idea,
            author=request.user,
            title=title,
            description=description,
            image=image,
            file=file
        )
        return redirect('idea_detail', pk=idea.pk)
    
    return render(request, 'innovation/add_solution.html', {'idea': idea})



@login_required
def delete_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    idea_pk = solution.idea.pk
    if solution.author == request.user:
        solution.delete()
    return redirect('idea_detail', pk=idea_pk)