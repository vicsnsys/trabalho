import time
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError


SIGLAS_ESTADOS = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
        'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo')
]

TURNO_CHOICES = [
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
        ('Integral', 'Integral')
]

GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino')
]


class Medico(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome Completo')
    crm = models.CharField(max_length=100, unique=True, verbose_name='CRM', help_text='Digite a CRM')
    telefone = models.CharField(max_length=11, unique=True, verbose_name='Telefone', help_text='Digite o telefone')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email', help_text='Digite o email')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', help_text='Data de Nascimento')
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF', help_text='Digite o CPF')
    turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name='Status', help_text='Selecione o Status')

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()

        if len(self.crm) < 8 or not self.crm[:-2].isdigit() or self.crm[-2:] not in SIGLAS_ESTADOS:
            raise ValidationError({'crm': 'Formato inválido. Tente: 000000UF (UF = sigla do estado)'})

        if len(self.telefone) != 11 or not self.telefone.isdigit():
            raise ValidationError("Inválido. O telefone deve ter 11 dígitos numéricos. Ex: 34912345678")

        if self.data_nascimento > date.today():
            raise ValidationError("Inválido. A Data de Nascimento deve ser anterior a hoje.")

        if len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValidationError("Inválido. O CPF deve conter exatamente 11 dígitos numéricos.")

class Setor(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome do Setor de Atuação')

    class Meta:
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not isinstance(self.nome, str):
            raise ValidationError("O nome do Setor deve ser do tipo String")

class Enfermeiro(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome Completo')
    coren = models.CharField(max_length=100, verbose_name='Coren', help_text='Digite o COREN')
    setor = models.ForeignKey(Setor, verbose_name='Setor', on_delete=models.RESTRICT)
    tele = models.CharField(max_length=11, unique=True, verbose_name='Telefone', help_text='Digite o telefone')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email', help_text='Digite o email')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', help_text='Data de Nascimento')
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF', help_text='Digite o CPF')
    turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name='Status', help_text='Selecione o Status')

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()

        if len(self.coren) < 8 or not self.coren[:-2].isdigit() or self.coren[-2:] not in SIGLAS_ESTADOS:
            raise ValidationError({'coren': 'Formato inválido. Tente: 000000UF (UF = sigla do estado)'})

        if len(self.tele) != 11 or not self.tele.isdigit():
            raise ValidationError("Erro. O telefone deve conter 11 dígitos numéricos.")

        if self.data_nascimento > date.today():
            raise ValidationError("Inválido. A Data de Nascimento deve ser anterior a hoje.")

        if len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValidationError("Inválido. O CPF deve conter exatamente 11 dígitos numéricos.")


class Paciente(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=10, choices=GENERO_CHOICES)
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF', help_text='Digite o CPF')
    rg = models.CharField(max_length=9, unique=True, verbose_name='RG', help_text='Digite o RG')
    nome_mae = models.CharField(max_length=100, verbose_name='Nome da Mãe', help_text='Nome Completo da Mãe')
    nome_pai = models.CharField(max_length=100, verbose_name='Nome do Pai (Opcional)', help_text='Nome Completo do Pai (Opcional)', blank=True, null=True)
    telefone_principal = models.CharField(max_length=11, verbose_name='Telefone', help_text='Digite o Telefone')
    telefone_secundario = models.CharField(max_length=11, verbose_name='Telefone Secundário', help_text='Digite o Segundo Telefone (Opcional)', blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name='Email', help_text='Digite o Email')
    tipo_sanguineo = models.CharField(max_length=2, verbose_name='Tipo Sanguíneo', help_text='Digite o Tipo Sanguíneo')

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()

        if self.data_nascimento > date.today():
            raise ValidationError("Inválido. A Data de Nascimento deve ser anterior a hoje.")

        if len(self.telefone_principal) != 11 or not self.telefone_principal.isdigit():
            raise ValidationError("Erro. O telefone principal deve conter 11 dígitos numéricos.")

        if self.telefone_secundario:
            if len(self.telefone_secundario) != 11 or not self.telefone_secundario.isdigit():
                raise ValidationError("Erro. O telefone secundário deve conter 11 dígitos numéricos.")

        if len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValidationError("Inválido. O CPF deve conter 11 dígitos numéricos.")

        if len(self.rg) != 9 or not self.rg.isdigit():
            raise ValidationError("Inválido. O RG deve conter 9 dígitos numéricos.")

        if self.nome_pai and not isinstance(self.nome_pai, str):
            raise ValidationError("Erro. O nome do pai deve ser do tipo String.")

        if len(self.tipo_sanguineo) != 2:
            raise ValidationError("Inválido. O tipo sanguíneo deve ter exatamente 2 caracteres.")
