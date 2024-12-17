from django.core.management.base import BaseCommand
import time
import os
from django.conf import settings
from datetime import datetime
import math
import pytz

class Command(BaseCommand):
    help = 'Descripción del comando'

    def handle(self, *args, **kwargs):
        carpeta = settings.MEDIA_ROOT
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.pdf'):
                os.remove(os.path.join(carpeta, archivo))
                print(f'Archivo borrado: {archivo}')