from celery.canvas import group, chord, chain
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

from core.tasks import send_mail, count_items, total_callback


class TasksView(TemplateView):
    template_name = 'core/send_tasks.html'

    def post(self, request):
        mytask = request.POST.get('task')
        if mytask == 'send_mail':
            task = send_mail.delay()
            return HttpResponse('tarea creada {}'.format(task.id))

        elif mytask == 'group_test':

            signatures = [send_mail.s(i) for i in range(20)]
            mygroup = group(signatures)
            group_result = mygroup()

            return HttpResponse('grupo creado {}'.format(group_result.id))

        elif mytask == 'chord_test':

            data = [
                [2, 7, 9, 33, 9, 8, 4, 3, 2],
                [5, 7, 9, 33, 7, 8, 9, 3, 2],
                [7, 7, 7, 33, 7, 8, 9, 8, 4, 3, 2],
                [3, 8, 4, 3, 2],
                [1, 7, 9, 33, 15, 56, 7, 8, 9, 8, 4, 3, 2],
                [9, 7, 3, 33, 37, 87, 9, 68, 74, 83, 92]
            ]

            signatures = [count_items.s(item) for item in data]

            mychord = chord(signatures)(total_callback.s())
            return HttpResponse('chord creado {}'.format(mychord.id))
