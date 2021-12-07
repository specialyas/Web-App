from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
	path("", views.homepage, name="homepage"),
	path("products", views.products, name = "products"),
	path("register", views.register, name="register"),
	path("login", views.login_request, name="login"),
	path("logout", views.logout_request, name="logut"),
	path("blog", views.blog, name='blog'),
	path("<article_page>", views.article, name="article"),
]