from celery.task import task
import time


@task
def send_mail():
    time.sleep(2)
    print('mail enviado')
