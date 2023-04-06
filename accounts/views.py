from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, FormView, DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import CustomUserCreationForm, CustomerPhotoForm
from .models import CustomUser


# A view that renders a form to register a new user. On successful submission,
# it creates a new user and redirects to the login page.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

# A simple view that renders a form for users to submit a contact request.
class ContactFormView(TemplateView):
    template_name = "registration/contact_form.html"


#  A view that displays the profile page for a specific user, along with
#  a form to upload a profile picture.
class PhotoGet(DetailView):
    model = CustomUser
    template_name = "accounts/profile_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerPhotoForm()
        return context

# A view that handles the submission of the profile picture form for a specific user.
# It saves the picture to the database and redirects to the profile page.
class ImagePost(SingleObjectMixin, FormView):
    model = CustomUser
    form_class = CustomerPhotoForm
    template_name = "accounts/profile_page.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.object
        if 'photo' in self.request.FILES:
            photo.photo = self.request.FILES['photo']
        photo.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.get_object()
        return reverse("profile", kwargs={"pk": user.pk})

# A view that handles both GET and POST requests for the profile page.
# On a GET request, it displays the profile page for the user.
# On a POST request, it handles the submission of the profile picture form.
class ProfilePage(View):

    def get(self, request, *args, **kwargs):
        view = PhotoGet.as_view()
        return view(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        view = ImagePost.as_view()
        return view(request, *args, **kwargs)