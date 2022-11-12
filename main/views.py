from django.shortcuts import render
from .forms import  PostForm, SearchForm, MyRegisterForm, CommentForm, EditForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from .models import Blog, Comments, Likers
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    returnedBlogs = []
    form=SearchForm(request.POST)

    likers = []
    if request.user.is_authenticated:
        likers = Likers.objects.filter(user = request.user)
    #now get the blogs from likers :
    liked_blogs = []
    for like in likers:
        liked_blogs.append(like.blog)


    if request.method == "POST":
        tag = request.POST["tag"]

        tags= tag.split(", ") # split into multiple tags
        for tag in tags:
            for blog in Blog.objects.all():
                if blog.tags.filter(name=tag):
                    returnedBlogs.append(blog)

        returnedBlogs = list(dict.fromkeys(returnedBlogs)) # to remove duplicates


        return render(request, "main/index.html",{
            "form":form,
            "user":request.user,
            "blogs":returnedBlogs,
            "liked_blogs": liked_blogs,
            "tags": tags
        })
    else:
        form=SearchForm()
        return render(request, "main/index.html",{
            "form": form,
            "user": request.user,
            "blogs": blogs,
            "liked_blogs": liked_blogs,
        })


def register(request):
    if request.method == "POST":
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #auto login after registration:
            new_user=authenticate(username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("/")
        return render(request, "main/register.html", {
            "form":form
        })
    else:
        form = MyRegisterForm()
        return render(request, "main/register.html", {
            "form": form
        })


def blog(request, blog_id):
    if Blog.objects.get(id=blog_id):

        blog = Blog.objects.get(id=blog_id)

        #see if the user liked the post or not
        liked=False
        if request.user.is_authenticated:
            if Likers.objects.filter(user=request.user, blog=blog).exists():
                liked = True
            else:
                liked = False   
        
        if request.method == "POST":

            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data["comment"]
                newComment = Comments.objects.create(blog=blog,user=request.user, text=comment)
                newComment.save()
            form = CommentForm()
            comments = blog.blog_comments.all() #related name for FK is
            #blog_comments so now I can access all related comments
            num = len(comments)
            return render(request, "main/blog.html",{
                "form": form,
                "blog": blog,
                "comments": comments,
                "num": num,
                "liked": liked
            })
        else:
            user = User.objects.get(username = blog.user.username)
            if request.user == user:
                okToEdit = True
            else:
                okToEdit = False
            form = CommentForm()
            comments = blog.blog_comments.all() #related name for FK is
            #blog_comments so now I can access all related comments
            num = len(comments)
            return render(request, "main/blog.html",{
            "form": form,
            "blog": blog,
            "comments": comments,
            "num": num,
            "okToEdit":okToEdit,
            "liked": liked
        })


def create(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            
            txt=form.cleaned_data["text"]
            title=form.cleaned_data["title"]
            url=form.cleaned_data["url"]
            tgs= form.cleaned_data["tags"].split(", ")
            #tgs2 = tuple(tgs)
            #date ???
            #likes?
            blog= Blog.objects.create(user=request.user,title=title, text=txt,url=url, likes=0)
            #blog = Blog(user=request.user,title=title, text=txt,url=url, likes=0)
            blog.save()
            for tg in tgs:
                blog.tags.add(tg)
                blog.save()
            blog.save()
            form = PostForm()
        return redirect("/")
    else:
        form = PostForm()
        return render(request, "main/create.html", {
            "form": form
        })



def edit(request, blog_id):
    #get the specific blog and prepopulate the form
    blog= Blog.objects.get(id=blog_id)

    if request.user == blog.user:
        tags = blog.tags.all()
        tgs=[]

        if request.method == "POST":

            form = EditForm(request.POST)
            if form.is_valid():
                blog= Blog.objects.get(id=blog_id)

                txt=form.cleaned_data["text"]
                title=form.cleaned_data["title"]
                url=form.cleaned_data["url"]
                tgs= form.cleaned_data["tags"].split(", ")
                #update all fields:
                blog.title = title
                blog.text = txt
                blog.url=url
                #first remove all tags:
                for tg in blog.tags.all():
                    blog.tags.remove(tg)
                blog.save()
                #now add the new tags:
                for tg in tgs:
                    blog.tags.add(tg)
                    blog.save()
                blog.save()
                form = EditForm()
            return redirect("blog", blog_id=blog.id)
        else:
            for tag in tags:    
                tgs.append(tag)

            form = EditForm({ "title": blog.title, "url": blog.url,
            "text": blog.text, "tags": tgs })
            return render(request, "main/edit.html", {
                "form": form
            })
    else:
        return redirect("/")

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    #only the creator of the blog can delete it
    if request.user == blog.user:
        blog.delete()
    else:
        return redirect("/")

    return redirect("/")


def like(request, blog_id):
    
    
    blog = Blog.objects.get(id = blog_id)
    if request.user.is_authenticated:
        likes= blog.likes
        if Likers.objects.filter(user=request.user, blog=blog).exists():
            liker = Likers.objects.get(user=request.user, blog=blog)
            liker.delete()
            blog.likes = likes - 1
            blog.save()
        else:
            liked = Likers.objects.create(user = request.user, blog = blog)
            blog.likes = likes + 1
            liked.save()
            blog.save()

    return redirect (f"/#{blog.id}")


def like2(request, blog_id):
    
    
    blog = Blog.objects.get(id = blog_id)
    if request.user.is_authenticated:
        likes= blog.likes
        if Likers.objects.filter(user=request.user, blog=blog).exists():
            liker = Likers.objects.get(user=request.user, blog=blog)
            liker.delete()
            blog.likes = likes - 1
            blog.save()
        else:
            liked = Likers.objects.create(user = request.user, blog = blog)
            blog.likes = likes + 1
            liked.save()
            blog.save()

    return redirect("blog", blog_id=blog.id)