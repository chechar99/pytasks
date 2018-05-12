from celery import group
from celery.canvas import chord
from celery.task import task
from django.core.paginator import Paginator
import time


@task
def send_mail():
    time.sleep(2)
    print('mail enviado')


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


@task
def complex_canvas(file_formatters, object_ids, operation):
    for file_formatter in file_formatters:
        object_set = file_formatter().get_objects(object_ids)
        signatures = []
        list_of_chords = []
        paginator = Paginator(object_set, BATCH_SIZE)
        for page in paginator.page_range:
            signatures.append(generate_files_lines.s(paginator.page(page).object_list, file_formatter))
            job = group(signatures)
            callback = finish_build_file.s(file_formatter)
            list_of_chords.append(chord(job, callback))
    chain_task = group(list_of_chords) | add_files_to_zip.s(operation)
    chain_task()


@task
def generate_files_lines(batch, file_formatter):
    lines = file_formatter.build_buffer(batch)
    return lines


@task
def finish_build_file(array_of_lines, file_formatter):
    file_body = ''
    for lines in array_of_lines:
        file_body += lines

    file_formatter.create_file(file_body)


@task(name='bulk.escrow.add_files_to_zip', ignore_result=False)
def add_files_to_zip(result, operation):
    OperationManager.make_zip(operation)
