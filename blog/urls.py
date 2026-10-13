from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]