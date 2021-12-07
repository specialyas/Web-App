from django.shortcuts import render, redirect
from .models import Product, Article
from django.core.paginator import Paginator
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def homepage(request):
	product = Product.objects.all()[:4]
	new_posts = Article.objects.all().order_by('-article_published')[:4]
	featured = Article.objects.filter(article_tags__tag_name='Featured')[:3]
	most_recent = new_posts.first()
	return render(request = request, template_name='main/home.html', context={'product':product, 'most_recent':most_recent, "new_posts":new_posts, "featured":featured})

def products(request):
	products = Product.objects.all()
	paginator = Paginator(products, 18)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request = request, template_name='main/products.html', context = {"page_obj": page_obj})
	
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccesful registrattion. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="main/register.html", context={"form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return  redirect('main:homepage')
			else: 
				messages.error(request, "Invalid username or password.")
		else: 
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, f"You have successfully logged out.")
	return  redirect('main:homepage')

def blog(request):
	blog = Article.objects.all().order_by('-article_published')
	paginator = Paginator(blog, 25)
	page_number = request.GET.get('page')
	blog_obj = paginator.get_page(page_number)
	return render(request=request, template_name="main/blog.html", context={"blog":blog_obj})


def article(request, article_page):
	article = Article.objects.get(article_slug=article_page)
	return render(request=request, template_name='main/article.html', context={"article": article})


