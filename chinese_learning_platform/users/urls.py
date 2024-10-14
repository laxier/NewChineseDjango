from django.urls import path, include, reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('frontend:index'),
        ),
        name='registration',
    ),
]
