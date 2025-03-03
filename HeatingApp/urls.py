from django.urls import path

from . import views

app_name = "HeatingApp"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("info/", views.InfoView.as_view(), name="info"),
    path("timers/", views.TimersView.as_view(), name="timers"),
    path("edit_timer/<int:pk>/", views.EditTimerView.as_view(), name="edit_timer"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("update_target_temperature/", views.update_target_temperature, name="update_target_temperature"),
    path("create_timer/", views.CreateTimerView.as_view(), name="create_timer"),
    path("create_timer_form/", views.create_timer_form, name="create_timer_form"),
    path("delete_timer/<int:pk>/", views.delete_timer, name="delete_timer"),
    path("update_current_temperature/<int:temperature>/<int:humidity>", views.update_current_temperature, name="update_current_temperature"),
]