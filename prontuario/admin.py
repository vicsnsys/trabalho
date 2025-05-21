from django.contrib import admin
from .models import Medico
from .models import Enfermeiro
from .models import Setor
from .models import Paciente

@admin.register(Medico)

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm' , 'status')

@admin.register(Enfermeiro)
class EnfermeiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'coren', 'status')

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Paciente)
class Paciente(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'tipo_sanguineo', 'data_nascimento')
