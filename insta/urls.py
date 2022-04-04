from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path,include
from django.conf import settings
from django.contrib.auth import views 
from . import views
from django_registration.backends.one_step.views import RegistrationView



urlpatterns=[
    re_path('^$',views.home,name = 'home'),
    re_path(r'^image/',views.display_image,name='displayImages'),
    re_path(r'^search/', views.search_results, name='search_results'),
    re_path('accounts/', include('django_registration.backends.one_step.urls')),
    re_path('accounts/register/',
        RegistrationView.as_view(success_url='/profile/'),
        name='django_registration_register'),
    # re_path(r'^accounts/logout/', views.logout, {"next_page": '/'}), 
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'profile/(?P<profile>[a-zA-Z0-9]+)$', views.get_user_profile,name='get_user_profile'),
    re_path('profile/<str:username>/',views.profile,name='profile'),
    re_path('user_profile/<username>/', views.user_profile, name='user_profile'),
    re_path(r'^new/image$', views.new_image, name='new_image'),
    re_path(r'like/<int:pk>', views.get_context_data, name='like_post'),
    re_path(r'follow_count',views.follow_count,name='follow_count'),
    re_path(r'BlogPostLike/<int:pk>', views.BlogPostLike, name='BlogPostLike'),

    

   
]




if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)