from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse
from django import forms
from django.contrib.auth.models import User
from .models import Image,Profile,NewsLetterRecipients,Comment,User,Follow
from .forms import NewsLetterForm, NewArticleForm
from django.contrib.auth.decorators import login_required
from .forms import UploadForm,ProfileForm,UpdateUserForm,UpdateUserProfileForm,CommentForm
from django.urls import reverse
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .email import send_welcome_email
from django.views.generic.detail import DetailView


class BlogPostDetailView(DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Image, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return  data
    
def BlogPostLike(request,pk):

    post = get_object_or_404(Image, id=request.POST.get('blogpost_id'),pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('BlogPostLike', args=[str(pk)]))

@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.GET.get('user')
    logged_in_user = request.user.username
    user_followers =len(Follow.objects.filter(user=current_user))
    user_following =len(Follow.objects.filter(follower=current_user))
    user_followers0 =Follow.objects.filter(follower=current_user)
    user_followers1 = []
    
    for i in user_followers0:
        user_followers0 = i.follower
        user_followers1.append(user_followers0)
    if logged_in_user in user_followers1:
        follow_button_value ='unfollow'
    else:
        follow_button_value = 'follow'
        
        
    profile = Profile.objects.all()
    image = Image.objects.all()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('home')
    else:
        form = NewsLetterForm()
    return render(request, 'home.html',{
        'profile':profile,
        'image':image,
        "letterForm":form,
        'current_user': current_user,
        'user_followers':user_followers,
        'user_following':user_following,
        'follow_button_value': follow_button_value,
        })
    
def post_detailview(request, id):
   
  if request.method == 'POST':
    cf = CommentForm(request.POST or None)
    if cf.is_valid():
      content = request.POST.get('content')
      comment = Comment.objects.create(user = request.user, content = content)
      comment.save()
      return redirect
    else:
      cf = CommentForm()
       
    context ={
      'comment_form':cf,
      }
    # return render(request, 'BlogPostLike', context)
    return HttpResponseRedirect(reverse('BlogPostLike',context))

def get_context_data(request,*args, **kwargs):
    context = super(home).get_context_data(request,*args,)
    stuff = get_object_or_404(Image,id=kwargs['pk'])
    total_likes = stuff.total_likes()
    context['total_likes'] = total_likes
    return context

def display_image(request):
    image = Image.objects.all()
 
    return render(request,'all-images.html',{'image':image})


def search_results(request):
    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        results = Image.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"images": results})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.profile = current_user
            article.save()
        return redirect('home')

    else:
        form = NewArticleForm()
    return render(request, 'new_image.html', {"form": form})

def get_user_profile(request, profile):
    user = Profile.objects.get(profile=profile)
    return render(request, 'user_profile.html', {"user":user})

@login_required(login_url='/accounts/login/')
def profile(request):
    images = request.user.profile.images.all()
    print(images)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'images': images,
    }
    return render(request, 'profile.html', params)

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('profile')
    else:
        form = UploadForm()
    return render(request,'edit_profile.html',{"form":form})
@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.images.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    return render(request, 'user_profile.html', params)
def like( request,pk):
    image = get_object_or_404(image, id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return HttpResponseRedirect(reverse('home', args=[str(pk)]))

def follow_count(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        user = request.POST.get('user')
        follower = request.POST.get('follower')
        if value == 'follow':
            followers_cnt = Follow.objects.create(user=user, follower=follower)
            followers_cnt.save()
        else:
            followers_cnt = Follow.objects.get(user=user, follower=follower)
            followers_cnt.delete()
        return redirect('/?user='+user)