from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app routes
    path('users/', include('users.urls')),
    path('', include('users.urls')),

    # Startups app routes
    path('startups/', include('startups.urls')),

    # Dashboard view
    path("dashboard/", TemplateView.as_view(template_name="startup_dashboard.html"), name="dashboard"),

    # Allauth (Google OAuth) routes
    path("accounts/", include("allauth.urls")),

    # .well-known/appspecific/com.chrome.devtools.json
    path('.well-known/appspecific/com.chrome.devtools.json', lambda request: JsonResponse({})),
]


