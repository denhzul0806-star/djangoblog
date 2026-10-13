
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from .models import Post, Category
from .forms import PostForm, RegistrationForm


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 6


def post_list(request):
    posts = Post.objects.filter(
        status="published"
    ).order_by("-created_at")

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj},
    )


def home(request):
    categories = Category.objects.all().order_by("name")
    posts = (
        Post.objects.filter(status="published")
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    return render(
        request,
        "blog/home.html",
        {"categories": categories, "posts": posts},
    )


def category_posts(request, slug):
    category_names = {
        "travel-around-niigata": "Travel Around Niigata",
        "niigata-station-izakaya": "Niigata Station Izakaya",
        "food": "Food",
        "restaurant": "Restaurant",
        "niigata-sea": "Niigata Sea",
    }

    name = category_names.get(slug)
    if not name:
        raise Http404("Category not found")

    category = get_object_or_404(Category, name__iexact=name)

    posts = (
        Post.objects.filter(
            status="published",
            category=category,
        )
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    return render(
        request,
        "blog/category.html",
        {"category": category, "posts": posts},
    )


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("category", "author").prefetch_related("tags"),
        slug=slug,
        status="published",
    )

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def base(request):
    return render(request, "blog/base.html")


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            "Post created successfully.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug},
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def get_object(self, queryset=None):
        post = get_object_or_404(
            Post,
            slug=self.kwargs["slug"],
        )

        if post.author_id != self.request.user.id:
            raise PermissionDenied

        return post

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug},
        )


@login_required(login_url="login")
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author_id != request.user.id:
        raise PermissionDenied

    if request.method == "POST":
        post.delete()
        messages.success(
            request,
            "Post deleted successfully.",
        )
        return redirect("home")

    return render(
        request,
        "blog/post_confirm_delete.html",
        {"post": post},
    )


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {"form": form},
    )


@login_required(login_url="login")
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author_id != request.user.id:
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            form.save()
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {"form": form, "object": post},
    )


def custom_403(request, exception=None):
    return render(
        request,
        "blog/403.html",
        status=403,
    )
