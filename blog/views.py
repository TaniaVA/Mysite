from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse

from .models import Blog
from .forms import CommentForm


# Create your views here.
class BlogListView(ListView):
    """
    Display a list of all Blog objects.

    Returns:
    A rendered ListView of Blog objects.
    """
    model = Blog
    template_name = "blog_list.html"

class CommentGet(DetailView):
    model = Blog
    template_name = "blog_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView):
    model = Blog
    form_class = CommentForm
    template_name = "blog_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.blog = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        blog = self.get_object()
        return reverse("blog_detail", kwargs={"pk": blog.pk})

class BlogDetailView(DetailView):
    """
    Display a detailed view of a single Blog object.

    Returns:
    A rendered DetailView of a single Blog object.
    """
    model = Blog
    template_name = "blog_detail.html"

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Blog object.

    Returns:
    A rendered CreateView of a new Blog object.
    """
    model = Blog
    template_name = "blog_new.html"
    fields = ['title', 'author', 'body',]

<<<<<<< HEAD

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
=======
class BlogUpdateView(UpdateView):
>>>>>>> function
    """
    Update an existing Blog object.

    Returns:
    A rendered UpdateView of an existing Blog object.
    """
    model = Blog
    template_name = "blog_edit.html"
    fields = ['title', 'body',]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing Blog object.

    Returns:
    A rendered DeleteView of an existing Blog object.
    """
    model = Blog
    template_name = "blog_delete.html"
    success_url = reverse_lazy("blog_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user