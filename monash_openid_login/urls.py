from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(),
        name='tardis.apps.monash.views.migrate_accounts'),
    url(r'^check-account-migration/$', views.check_account_migration,
        name='tardis.apps.monash.views.check_account_migration')
]
