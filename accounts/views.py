from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages

from accounts.forms import WorkerRegistrationForm, LoginForm, UserForm, ProfileForm
from accounts.models import Profile
from task_manager.models import Worker, TaskType, Task

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("task_manager:tasks"))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {'form': form})


def register_worker(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_manager:tasks')
    else:
        form = WorkerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


class WorkerProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """DetailView class for user profile page."""

    model = Worker
    template_name = "accounts/worker_profile_detail.html"


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/user_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['profile'] = user.profile if hasattr(user, 'profile') else None

        task_types = TaskType.objects.all()
        context['task_counts'] = {
            task_type.name: Task.objects.filter(task_type=task_type, assignees=user).count()
            for task_type in task_types
        }

        context['completed_tasks_count'] = Task.objects.filter(assignees=user, is_completed=True).count()
        context['uncompleted_tasks_count'] = Task.objects.filter(assignees=user, is_completed=False).count()

        return context


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'accounts/user_profile_update_form.html'
    form_class = UserForm
    second_form_class = ProfileForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile, created = Profile.objects.get_or_create(worker=user)  # Ensure profile exists
        context['profile'] = profile
        if 'profile_form' not in context:
            context['profile_form'] = self.second_form_class(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.second_form_class(request.POST, instance=request.user.profile)

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect(reverse('accounts:user_profile'))  # Redirect to the profile page

    def form_invalid(self, form, profile_form):
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = 'accounts/user_delete_confirm.html'
    success_url = reverse_lazy('task_manager:index')  # Redirect to the home page or a custom page after deletion

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your account has been deleted.")
        return super(UserDeleteView, self).delete(request, *args, **kwargs)