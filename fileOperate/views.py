import coloredlogs
import logging
import os

from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

from .utils import get_FileSize, get_ip

SAVED_FILES_DIR = settings.SAVED_FILES_DIR

coloredlogs.install(level='DEBUG')
coloredlogs.install(fmt='%(asctime)s [%(process)d] %(levelname)s: %(message)s')
# formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
# sh = logging.StreamHandler()
# sh.setFormatter(formatter)
# sh.setLevel(logging.DEBUG)
logger = logging.getLogger(__file__)
# logger.addHandler(sh)
# logger.setLevel(logging.DEBUG)

def render_home_template(request):
    files = []
    all_files_name = os.listdir(SAVED_FILES_DIR)  # 读取文件夹下的所有文件名
    for file_name in all_files_name:
        if file_name.endswith('.pdf'):  # 判断是否为PDF文件名
            file_info = file_name.split('-')
            student_number = file_info[0]
            student_name = file_info[-1]
            student_name = student_name.strip('.pdf')
            file_size = get_FileSize(os.path.join(SAVED_FILES_DIR, file_name))

            file = {
                'number': student_number,
                'name': student_name,
                'file_name': file_name,
                'file_size': file_size,
            }

            files.append(file)

    return render(request, 'fileOperate/home.html', {'files': files})


@require_GET
def index(request):
    if not os.path.exists(SAVED_FILES_DIR):
        os.makedirs(SAVED_FILES_DIR)

    return render_home_template(request)


@require_GET
def download(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR, filename)

    client_ip = get_ip(request)
    logger.info(f'IP: {client_ip} have downloaded file {filename}')

    with open(file_pathname, 'rb') as f:
        file = File(f)

        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response

