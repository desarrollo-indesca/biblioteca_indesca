from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Informe, Descriptor, Empresa
from biblioteca_digital.settings import BASE_DIR
import csv
import openpyxl

class Command(BaseCommand):
    help = "Carga los libros en la base de datos junto a los posibles descriptores"

    def handle(self, *args, **options):
        print(BASE_DIR.__str__() + "\\INFORMES.xlsx")
        dataframe = openpyxl.load_workbook(BASE_DIR.__str__() + "\\INFORMES.xlsx")['INFORMES']
        dataframe.active = True
        with transaction.atomic():
                for row in dataframe.iter_rows(2, dataframe.max_row):
                    informe = Informe()
                    ano = str(row[9].value).strip()
                    ano = ano if ano != '' else None

                    informe.no_registro = str(row[0].value).strip()
                    informe.programa = Empresa.objects.get_or_create(nombre=str(row[1].value).strip())[0]
                    informe.codigo_proyecto = str(row[2].value).strip()
                    informe.ano_publicacion = ano
                    informe.titulo = str(row[7].value).strip()
                    informe.autores = str(row[4].value).strip()
                    informe.solicitud_servicio = str(row[5].value).strip() if str(row[5].value).strip() != '' else None 

                    informe.save()

                    descriptores = []                    
                    for x in row[3].value.split(','):
                        x = x.strip().upper()
                        descriptor = Descriptor.objects.get_or_create(nombre=x)[0]
                        descriptores.append(descriptor)
                    
                    informe.descriptores.add(*descriptores)

                    informe.save()