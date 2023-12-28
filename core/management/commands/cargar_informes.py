from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Informe, Descriptor, Empresa
from biblioteca_digital.settings import BASE_DIR
import csv

class Command(BaseCommand):
    help = "Carga los libros en la base de datos junto a los posibles descriptores"

    def handle(self, *args, **options):
        with open(BASE_DIR.__str__() + "\\INfORMES.csv", 'r', encoding='unicode_escape') as file:
            reader = csv.reader(file,delimiter=';')
            next(reader)
            with transaction.atomic():
                for row in reader:
                    informe = Informe()
                    ano = row[9].strip()
                    ano = ano if ano != '' else None

                    informe.no_registro = row[0].strip()
                    informe.programa = Empresa.objects.get_or_create(nombre=row[1].strip())
                    informe.codigo_proyecto = row[2].strip()
                    informe.ano_publicacion = ano
                    informe.titulo = row[7].strip()
                    informe.autores = row[4].strip()
                    informe.solicitud_servicio = row[5].strip() if row[5].strip() != '' else None 

                    informe.save()

                    descriptores = []                    
                    for x in row[3].split(','):
                        x = x.strip().upper()
                        descriptor = Descriptor.objects.get_or_create(nombre=x)[0]
                        descriptores.append(descriptor)
                    
                    informe.descriptores.add(*descriptores)

                    informe.save()