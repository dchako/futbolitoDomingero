from django.conf.urls import patterns, include, url
from FutboolGruops.views import ExtraDataView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'FutboolGruops.views.home', name='home'),
    url(r'^homes/(?P<id>\d+)$', 'FutboolGruops.views.homes', name='homes'),
    url(r'^invitacion$', 'FutboolGruops.views.invitacion', name='invitacion'),
    url(r'^invitar/$', 'FutboolGruops.views.invitar', name='invitar'),
    url(r'^asistencia_ajax/$',
                'FutboolGruops.views.asistencia_ajax', name='asistencia_ajax'),
    url(r'^cambioDeEquipo_ajax/$',
        'FutboolGruops.views.cambioDeEquipo_ajax', name='cambioDeEquipo_ajax'),
    url(r'^invitar_ajax/$',
                     'FutboolGruops.views.invitar_ajax', name='invitar_ajax'),
    url(r'^login$', 'FutboolGruops.views.login', name='login'),
    url(r'^registrar$', ExtraDataView.as_view(), name='registrar'),
    #url(r'^registrar$', 'FutboolGruops.views.registrar', name='registrar'),
    url(r'^error$', 'FutboolGruops.views.error', name='error'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
)
