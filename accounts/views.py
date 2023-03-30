from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

class ContactFormView(TemplateView):
    template_name = "registration/contact_form.html"

class ProfilePage(DetailView):
    model = CustomUser
    template_name = "accounts/profile_page.html"

class UpdateProfile(UpdateView):
    """
    Update an existing Profile object.

    Returns:
    A rendered UpdateView of an existing profile object.
    """
    model = CustomUser
    template_name = "profile_edit.html"
    fields = ['username', 'email', 'image', ]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        # Получаем объект блога из базы данных
        blog = form.save(commit=False)
        # Получаем загруженное изображение из формы
        image = form.cleaned_data['image']
        # Если загружено изображение, то сохраняем его в файловой системе
        if image:
            file_name = default_storage.save(image.name, ContentFile(image.read()))
            blog.image = file_name
        # Сохраняем изменения в базе данных
        blog.save()
        return super().form_valid(form)
