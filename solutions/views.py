from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Solution

# 1. Vitrin və Axtarış
def solutions_home(request):
    query = request.GET.get('search')
    if query:
        solutions = Solution.objects.filter(
            Q(title__icontains=query) | Q(target_area__icontains=query)
        ).order_by('-created_at')
    else:
        solutions = Solution.objects.all().order_by('-created_at')
    return render(request, 'solutions/solutions_home.html', {'solutions': solutions, 'query': query})

# 2. Yeni Həll Yaratmaq (Olduğu kimi qalır)
@login_required
def create_solution(request):
    if request.method == 'POST':
        Solution.objects.create(
            author=request.user,
            title=request.POST.get('title'),
            target_area=request.POST.get('target_area'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            technical_file=request.FILES.get('technical_file')
        )
        return redirect('solutions_home')
    return render(request, 'solutions/create_solution.html')

# 3. Detallar Səhifəsi
def solution_detail(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    return render(request, 'solutions/solution_detail.html', {'solution': solution})

# 4. Həlli Silmək (Ancaq özününkünü)
@login_required
def delete_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk, author=request.user)
    solution.delete()
    return redirect('solutions_home')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Solution, Comment

# Səsvermə funksiyası
@login_required
def vote_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    if solution.votes.filter(id=request.user.id).exists():
        solution.votes.remove(request.user)
    else:
        solution.votes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'solutions_home'))

# Şərh yazmaq funksiyası
@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        solution = get_object_or_404(Solution, pk=pk)
        text = request.POST.get('comment_text')
        parent_id = request.POST.get('parent_id') # Cavab verilən şərhin ID-si
        
        parent_obj = None
        if parent_id:
            parent_obj = Comment.objects.get(id=parent_id)
            
        if text:
            Comment.objects.create(
                solution=solution, 
                user=request.user, 
                text=text, 
                parent=parent_obj
            )
    return redirect('solution_detail', pk=pk)