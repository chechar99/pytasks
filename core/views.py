from celery.canvas import group
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

from core.tasks import send_mail


class TasksView(TemplateView):
    template_name = 'core/send_tasks.html'

    def post(self, request):
        mytask = request.POST.get('task')
        if mytask == 'send_mail':

            task = send_mail.delay('prueba')
            return HttpResponse('tarea creada {}'.format(task.id))

        elif mytask == 'group_test':

            signatures = [send_mail.s(i) for i in range(20)]
            mygroup = group(signatures)
            group_result = mygroup()

            return HttpResponse('grupo creado {}'.format(group_result.id))
