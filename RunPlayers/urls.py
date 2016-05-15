from django.conf.urls import patterns, include, url
from FutboolGruops.views import ExtraDataView
from rest_framework import routers
from FutboolGruops import views
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'jugadores', views.JugadoresViewSet)

router.register(r'Eventos', views.EventosViewSet)
#equipo_list_id = views.EquiposViewSet.as_view({'get': 'list'})
router.register(r'Equipos', views.EquiposViewSet)

router.register(r'Grupos', views.GruposViewSet)
router.register(r'Invitacion', views.InvitacionViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^(?P<id>\d+)$', 'FutboolGruops.views.home', name='home'),
    url(r'^$', 'FutboolGruops.views.home_2', name='home_2'),
    #url(r'^homes/(?P<id>\d+)$', 'FutboolGruops.views.homes', name='homes'),
    url(r'^invitar/(?P<id>\d+)$',
                        'FutboolGruops.views.invitar', name='invitar'),
    url(r'^estrategias/(?P<id>\d+)$',
                        'FutboolGruops.views.estrategias', name='estrategias'),
    url(r'^configurar/(?P<id>\d+)$',
                        'FutboolGruops.views.configurar', name='configurar'),
    url(r'^invitacion$', 'FutboolGruops.views.invitacion', name='invitacion'),
    #url(r'^invitar/$', 'FutboolGruops.views.invitar', name='invitar'),
    url(r'^asistencia_ajax/$',
                'FutboolGruops.views.asistencia_ajax', name='asistencia_ajax'),
    url(r'^cambioDeEquipo_ajax/$',
        'FutboolGruops.views.cambioDeEquipo_ajax', name='cambioDeEquipo_ajax'),
    url(r'^invitar_ajax/$',
                     'FutboolGruops.views.invitar_ajax', name='invitar_ajax'),
    url(r'^cargar_goles/$',
                     'FutboolGruops.views.cargar_goles', name='cargar_goles'),
    url(r'^invitacion_ajax/$',
                'FutboolGruops.views.invitacion_ajax', name='invitacion_ajax'),
    url(r'^login$', 'FutboolGruops.views.login', name='login'),
    url(r'^registrar$', ExtraDataView.as_view(), name='registrar'),
    #url(r'^registrar$', 'FutboolGruops.views.registrar', name='registrar'),
    url(r'^error$', 'FutboolGruops.views.error', name='error'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
    #api
    url(r'^sociallogin/', 'FutboolGruops.views.social_register'),
    #url(r'^Equipos/(?P<pk>[0-9]+)$', equipo_list_id, name='eventos-detail'),
    url(r'^api/', include(router.urls))
)
