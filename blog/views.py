from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog


# Create your views here.
class BlogListView(ListView):
    """
    Display a list of all Blog objects.

    Returns:
    A rendered ListView of Blog objects.
    """
    model = Blog
    template_name = "blog_list.html"


class BlogDetailView(DetailView):
    """
    Display a detailed view of a single Blog object.

    Returns:
    A rendered DetailView of a single Blog object.
    """
    model = Blog
    template_name = "blog_detail.html"


class BlogCreateView(CreateView):
    """
    Create a new Blog object.

    Returns:
    A rendered CreateView of a new Blog object.
    """
    model = Blog
    template_name = "blog_new.html"
    fields = ['title', 'author', 'body',]


class BlogUpdateView(UpdateView):
    """
    Update an existing Blog object.

    Returns:
    A rendered UpdateView of an existing Blog object.
    """
    model = Blog
    template_name = "blog_edit.html"
    fields = ['title', 'body',]


class BlogDeleteView(DeleteView):
    """
    Delete an existing Blog object.

    Returns:
    A rendered DeleteView of an existing Blog object.
    """
    model = Blog
    template_name = "blog_delete.html"
    success_url = reverse_lazy("blog_list")