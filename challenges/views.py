from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Challenge, Submission
from .forms import SubmissionForm, ChallengeCreateForm

def challenge_list(request):
    # DÜZƏLİŞ 3: Yalnız təsdiqlənmiş və SİLİNMƏMİŞ (is_deleted=False) yarışları göstər
    challenges = Challenge.objects.filter(
        is_approved=True, 
        is_deleted=False
    ).order_by('-created_at')
    return render(request, 'challenges/list.html', {'challenges': challenges})

@login_required
def challenge_detail(request, pk):
    # Yalnız silinməmiş yarışın detallarına baxmaq olar
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True, is_deleted=False)
    
    # DÜZƏLİŞ 1: Submission-ların gizlədilməsi
    # Əgər baxan adam yarışı qoyandırsa hamısını görsün, iştirakçıdırsa yalnız özünkünü
    if challenge.organizer == request.user:
        submissions = challenge.submissions.all()
    else:
        submissions = challenge.submissions.filter(solver=request.user)

    user_submission = submissions.filter(solver=request.user).first()
    
    # DÜZƏLİŞ 2: Vaxtın bitməsini yoxla
    is_expired = timezone.now() > challenge.deadline
    
    leaderboard = None
    if challenge.status == 'FINISHED':
        leaderboard = challenge.submissions.all().order_by('-score', 'created_at')

    if request.method == 'POST':
        # Vaxt bitibsə və ya status aktiv deyilsə həll qəbul etmə
        if is_expired or challenge.status != 'ACTIVE':
            messages.error(request, "Bu yarış artıq həll qəbul etmir (Müddət bitib).")
            return redirect('challenge_detail', pk=pk)
            
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.challenge = challenge
            submission.solver = request.user
            submission.save()
            messages.success(request, "Həlliniz uğurla qeydə alındı!")
            return redirect('challenge_detail', pk=pk)
    else:
        form = SubmissionForm(instance=user_submission) if user_submission else SubmissionForm()

    context = {
        'challenge': challenge,
        'form': form,
        'user_submission': user_submission,
        'submissions': submissions, # Filterlənmiş siyahı
        'leaderboard': leaderboard,
        'is_expired': is_expired
    }
    return render(request, 'challenges/detail.html', context)

@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeCreateForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.organizer = request.user
            challenge.is_approved = False
            challenge.is_deleted = False # Yeni yarış silinməmiş kimi yaranır
            challenge.status = 'ACTIVE'
            challenge.save()
            messages.success(request, "Yarış uğurla yaradıldı! Admin təsdiqindən sonra canlıya keçəcək.")
            return redirect('challenge_list')
    else:
        form = ChallengeCreateForm()
    return render(request, 'challenges/create_challenge.html', {'form': form})

# DÜZƏLİŞ 3-ün davamı: Soft Delete funksiyası
@login_required
def delete_challenge(request, pk):
    # Yalnız yarışı yaradan adam "silə" bilsin
    challenge = get_object_or_404(Challenge, pk=pk, organizer=request.user)
    challenge.is_deleted = True
    challenge.save()
    messages.success(request, "Yarış uğurla silindi.")
    return redirect('challenge_list')

from .forms import GradeSubmissionForm

@login_required
def grade_submission(request, sub_pk):
    submission = get_object_or_404(Submission, pk=sub_pk, challenge__organizer=request.user)
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"{submission.solver.username} üçün qiymət qeyd olundu.")
            return redirect('challenge_detail', pk=submission.challenge.pk)
    
    return redirect('challenge_detail', pk=submission.challenge.pk)