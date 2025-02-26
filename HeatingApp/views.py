from django.shortcuts import render
from django.http import HttpResponse
from .models import Info, Timer
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'HeatingApp/index.html'
    context_object_name = 'info'

    def get_queryset(self):
        return Info.objects.get(pk=1)
    
    def post(self, request):
        print("test")
    
    
class InfoView(generic.ListView):
    template_name = 'HeatingApp/info.html'
    context_object_name = 'info'

    def get_queryset(self):
        return Info.objects.get(pk=1)

class TimersView(generic.ListView):
    template_name = 'HeatingApp/timers.html'
    context_object_name = 'timers'

    def get_queryset(self):
        return Timer.objects.all()[:5]
    
class EditTimerView(generic.ListView):
    template_name = 'HeatingApp/edit_timer.html'
    context_object_name = 'timer'
    model = Timer

    def get_queryset(self):
        return Timer.objects.get(pk=self.kwargs['pk'])

class SettingsView(generic.ListView):
    template_name = 'HeatingApp/settings.html'
    context_object_name = 'settings'

    def get_queryset(self):
        return
    
class CreateTimerView(generic.ListView):
    template_name = 'HeatingApp/create_timer.html'
    context_object_name = 'create_timer'

    def get_queryset(self):
        return
    
def update_target_temperature(request):
    if request.method != "POST":
        return render(request, 'HeatingApp/index.html', {})
    i = Info.objects.get(pk=1)
    i.target_temperature = request.POST["set-temperature"]
    i.save()
    return HttpResponse("""
<html>
    <head>
        <meta http-equiv="refresh" content="2;url=/heating_app" />
    </head>
    <body>
        <p>Temperature Updated successfully! You will be redirected shortly.</p>
    </body>
</html>
                        """)

def create_timer_form(request):
    if request.method != "POST":
        return render(request, 'HeatingApp/timers.html', {})
    t = Timer()
    t.start_time = request.POST["start-time"]
    t.end_time = request.POST["end-time"]
    t.target_temperature = request.POST["set-temperature"]
    t.active = False
    t.save()
    return HttpResponse("""
<html>
    <head>
        <meta http-equiv="refresh" content="2;url=/heating_app/timers/" />
    </head>
    <body>
        <p>Timer Created successfully! You will be redirected shortly.</p>
    </body>
</html>
                        """)

def delete_timer(request, pk):
    t = Timer.objects.get(pk=pk)
    t.delete()
    return HttpResponse("""
<html>
    <head>
        <meta http-equiv="refresh" content="2;url=/heating_app/timers/" />
    </head>
    <body>
        <p>Timer Deleted successfully! You will be redirected shortly.</p>
    </body>
</html>
                        """)