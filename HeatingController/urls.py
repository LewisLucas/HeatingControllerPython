from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("heating_app/", include("HeatingApp.urls")),
    path('admin/', admin.site.urls),
]
