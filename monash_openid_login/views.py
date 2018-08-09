from six.moves import urllib

from django.views.generic.base import TemplateView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import auth as djauth
from django.contrib.auth.models import User
from django.contrib import messages

from tardis.tardis_portal.forms import LoginForm
from tardis.tardis_portal.shortcuts import render_response_index


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, request, **kwargs):
        url = request.META.get('HTTP_REFERER', '/')
        u = urllib.parse.urlparse(url)
        if u.netloc == request.META.get('HTTP_HOST', ""):
            next_page = u.path
        else:
            next_page = '/'
        c = super(LoginView, self).get_context_data(**kwargs)
        c['loginForm'] = LoginForm()
        c['next_page'] = next_page
        return c

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect the user to the home page if he is trying to go to the
            # login page
            return HttpResponseRedirect(request.GET.get('next_page', '/'))

        c = self.get_context_data(request, **kwargs)
        return render_response_index(request, self.template_name, c)

    def post(self, request, *args, **kwargs):
        from tardis.tardis_portal.auth import auth_service
        c = self.get_context_data(request, **kwargs)
        if request.user.is_authenticated:
            # redirect the user to the home page if he is trying to go to the
            # login page
            return HttpResponseRedirect(request.POST.get('next_page', '/'))

        # TODO: put me in SETTINGS
        if 'username' in request.POST and \
                'password' in request.POST:
            authMethod = request.POST.get('authMethod', None)

            user = auth_service.authenticate(
                authMethod=authMethod, request=request)

            if user:
                next_page = request.POST.get(
                    'next_page', '/')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                djauth.login(request, user)
                return HttpResponseRedirect(next_page)

            if User.objects.filter(
                    username=request.POST['username'],
                    is_active=False).first():
                c['status'] = "Sorry, this account is inactive."
            else:
                c['status'] = "Sorry, username and password don't match."
            c['error'] = True
            c['loginForm'] = LoginForm()

            return HttpResponseForbidden(
                render_response_index(request, self.template_name, c))

        return render_response_index(request, self.template_name, c)


def check_account_migration(request):
    """
    This method is to be run after a successful AAF login, and should
    check whether the user already has an account with the same email
    address which needs to be migrated.
    """
    messages.add_message(request, messages.INFO,
        'Please click on your email address and select the '
        '"Migrate My Account" menu item to migrate your old account')
    return HttpResponseRedirect(request.GET.get('next_page', '/'))
