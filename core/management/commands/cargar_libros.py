from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Libro, Descriptor
from biblioteca_digital.settings import BASE_DIR
import csv

class Command(BaseCommand):
    help = "Carga los libros en la base de datos junto a los posibles descriptores"

    def handle(self, *args, **options):
        with open(BASE_DIR.__str__() + "\\Base de Datos de Libros.csv", 'r', encoding='unicode_escape') as file:
            reader = csv.reader(file,delimiter=';')
            next(reader)
            with transaction.atomic():
                for row in reader:
                    libro = Libro()
                    ano = row[0].strip()
                    ano = ano if ano != '' else None

                    cdcuter = row[4].strip()

                    libro.ano_publicacion = ano
                    libro.codigo = row[1].strip()
                    libro.cdinf = row[2].strip()
                    libro.cdlc = row[3].strip()
                    libro.cdcuter = cdcuter if cdcuter != "No Tiene" else None
                    libro.cddewey = row[5].strip()
                    libro.titulo = row[6].strip()
                    libro.autores = row[7].strip()

                    libro.save()

                    descriptores = []                    
                    for x in row[8].split(','):
                        x = x.strip().upper()
                        descriptor = Descriptor.objects.get_or_create(nombre=x)[0]
                        descriptores.append(descriptor)
                    
                    libro.descriptores.add(*descriptores)

                    libro.save()