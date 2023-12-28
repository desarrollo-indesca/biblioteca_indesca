from django.core.management.base import BaseCommand
from core.models import Empresa
from biblioteca_digital.settings import BASE_DIR

class Command(BaseCommand):
    help = "Carga las empresas de los informes en la base de datos"

    def handle(self, *args, **options):
        empresas = [
            Empresa(nombre='INDESCA'),
            Empresa(nombre='ESTIZULIA'),
            Empresa(nombre='PEQUIVEN'),
            Empresa(nombre='PETROPLAS'),
            Empresa(nombre='POLINTER'),
            Empresa(nombre='PRALCA'),
            Empresa(nombre='PROPILVEN'),
            Empresa(nombre='SUPERMETANOL'),
            Empresa(nombre='METOR'),
            Empresa(nombre='FERTINITRO'),
            Empresa(nombre='PDVSA'),
            Empresa(nombre='FERTILIZANTES DE ORIENTE'),
            Empresa(nombre='IDP'),
            Empresa(nombre='CLIENTES EXTERNOS'),
            Empresa(nombre='RESILIN'),
            Empresa(nombre='PLASTILAGO'),
            Empresa(nombre='POLILAGO')
        ]

        Empresa.objects.bulk_create(empresas)