from celery.task import task
import time


@task
def send_mail(body):
    time.sleep(2)
    print('mail enviado {}'.format(body))


@task
def sum_items(mylist):
    time.sleep(1)
    return sum(mylist)


@task
def count_items(mylist):
    time.sleep(1)
    return sum(mylist)


@task
def total_callback(results):
    time.sleep(1)
    return sum(results)
