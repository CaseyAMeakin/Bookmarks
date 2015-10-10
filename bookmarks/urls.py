from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<bookmark_id>[0-9]+)/$', views.detail,name='detail'),
    url(r'^(?P<bookmark_id>[0-9]+)/edit/$', views.edit,name='edit'),
    url(r'^(?P<bookmark_id>[0-9]+)/goto/$', views.gotolink,name='gotolink'),
    url(r'^(?P<bookmark_id>[0-9]+)/submitedit/$', views.submitedit,name='submitedit'),
    url(r'^add/$', views.addlink,name='addlink'),
    url(r'^signup/$', views.signup,name='signup'),
    url(r'^(?P<bookmark_id>[0-9]+)/bdelete/$', views.bdelete,name='bdelete'),
    url(r'^(?P<bookmark_id>[0-9]+)/bdelete_chk/$', views.bdelete_chk,name='bdelete_chk'),
    url(r'^enternew/$', views.enternew,name='enternew'),
    url(r'^search/$', views.search,name='search'),
    url(r'^home/$',views.home,name='home'),
    url(r'^userlogin/$',views.userlogin,name='userlogin'),
    url(r'^userlogout/$',views.userlogout,name='userlogout'),
]
