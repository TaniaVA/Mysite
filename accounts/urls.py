from django.urls import path
from .views import SignUpView, ContactFormView, ProfilePage

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('contact_form/', ContactFormView.as_view(), name='contact_form'),
    path("<int:pk>/", ProfilePage.as_view(), name="profile"),
]
