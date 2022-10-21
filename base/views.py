import random
from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import UserCreationForm,EditUser
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import User,Post,Like,Comment,follower_count
from itertools import chain

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('settings')
        else:
            messages.error(request,'Error has occured!')

    context={'form':form}
    return render(request,'base/register.html',context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('feed')
            else:
                messages.info(request,"Credential Invalid")


    return render(request,'base/login.html')
    
@login_required(login_url='login')
def settings(request):
    user=request.user
    form=EditUser(instance=user)
    if request.method=='POST':
        form=EditUser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('feed')

    context={'form':form}

    return render(request,'base/settings.html',context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def feed(request):
    # posts=Post.objects.all()
    # user=request.user
    user_following_list = []
    feed = []

    user_following = follower_count.objects.filter(viewing_user=request.user.username)

    for users in user_following:
        user_following_list.append(users.profile_user)

    user_following_list.append(request.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(auther__username=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
        
    
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.profile_user)
        user_following_all.append(user_list)
    user_following_all.append(request.user)

    new_suggested_user=User.objects.exclude(username__in=user_following_all)
    
    

    
    context={'posts':feed_list,'new_suggested_user':new_suggested_user}
    return render(request,'base/feed.html',context)


@login_required(login_url='login')
def uploadpost(request):
    if request.method=='POST':
        new_post=Post.objects.create(auther=request.user,
        postimage=request.FILES.get('image_upload'),
        caption=request.POST.get('caption')
        )
        new_post.save()
        return redirect ('feed')
    return render(request,'base/feed.html')
    

@login_required(login_url='login')
def likepost(request):
    post_id=request.GET.get('post_id')
    post_obj=Post.objects.get(id=post_id)

    if request.user in post_obj.liked.all():
        post_obj.liked.remove(request.user)
    else:
        post_obj.liked.add(request.user)

    like,created=Like.objects.get_or_create(viewer=request.user,post_id=post_id)
    if created:
        like.save()
        return redirect('feed')

    return redirect('feed')

@login_required(login_url='login')
def deletePost(request,pk):
    post=Post.objects.get(id=pk)
    if request.user!=post.auther:
        return HttpResponse('Youu are not allowed here!!')
    if request.method=='POST':
        post.delete()
        return redirect('feed')

    return render(request,'base/delete.html')



# @login_required(login_url='login')
# def commentpost(request):
    

#     if request.method=='POST':
#         post_id=request.POST.get('post_id')


#     post_obj=Post.objects.get(id=post_id)
#     comments=post_obj.comment_set.all()
#     if request.method=='POST':
#         new_comment=Comment.object.create(
#             commenter=request.user,
#             body=request.POST.get('body'),

#         )
#         new_comment.save()
#         return redirect('feed')
    
#     context={'comments':comments}
#     return render(request,'base/feed.html',context)

@login_required(login_url='login')
def searchuser(request):
    filtered_user=None
    if request.method=='POST':
        username=request.POST.get('username')
        filtered_user=User.objects.filter(username__icontains=username)
    return render(request,'base/search.html',{'filtered_users':filtered_user})

@login_required(login_url='login')
def userprofile(request,pk):
    user=User.objects.get(id=pk)
    posts=user.post_set.all()
    post_count=posts.count()
    viewing_user=request.user
    profile_user=user
    if follower_count.objects.filter(profile_user=profile_user,viewing_user=viewing_user):
        value='unfollow'
    else:
        value='follow'

    followingcount=follower_count.objects.filter(profile_user=user).count()
    followercount=follower_count.objects.filter(viewing_user=user).count()
    
    context={'user':user,'posts':posts,'post_count':post_count,'value':value,'followingcount':followingcount,'followercount':followercount}

    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def followerunfollow(request):
    if request.method=='POST':
        viewing_user=request.POST.get('viewing_user')
        profile_user=request.POST.get('profile_user')
        profile_id=request.POST.get('profile_id')
        
        if follower_count.objects.filter(viewing_user=viewing_user, profile_user=profile_user):
            delete_follower = follower_count.objects.get(viewing_user=viewing_user, profile_user=profile_user)
            delete_follower.delete()
            return redirect('userprofile',pk=profile_id)

        else:
            new_follower = follower_count.objects.create(viewing_user=viewing_user, profile_user=profile_user)
            new_follower.save()
            return redirect('userprofile',pk=profile_id)

    return render (request,'base/profile.html')

            
            





