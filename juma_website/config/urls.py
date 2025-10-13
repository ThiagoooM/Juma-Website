from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Juma import views  # 👈 importante

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Juma.urls')),

    path('accounts/login/', include('django.contrib.auth.urls')),
    path('accounts/logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
