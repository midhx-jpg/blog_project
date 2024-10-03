from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from blog.forms import SignUpForm,ProfileForm,BlogPostForm
from blog.models import BlogPost
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import BlogPostSerializer
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def index(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"base.html",{'page_obj': page_obj})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            form.save_m2m()
            return redirect(index)
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

# def blog_list(request):
    
#     return render(request, 'blog_list.html', )

@login_required
def blog_list_byuser(request):
    # Filter by the logged-in user
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Paginator setup: Show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog_list_byuser.html', {'page_obj': page_obj})

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class CustomLogoutView(LogoutView):
    template_name = 'logged_out.html'
    

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

def blog_detail_view(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'blog_detail.html', {'post': post})

def update_post_view(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})


def delete_post_view(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect(index)
    return render(request, 'delete_post.html', {'post': post})
