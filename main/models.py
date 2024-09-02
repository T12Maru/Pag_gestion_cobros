from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    ultimo_pago = models.TextField(db_column='ultimo_pago', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE',max_length=140, blank=True, null=True)
    apellidos = models.CharField(db_column='APELLIDO',max_length=140, blank=True, null=True)
    direccion = models.CharField(db_column='DIRECCION',max_length=140, blank=True, null=True)
    cod_post = models.IntegerField(db_column='CODIGO_POS', blank=True, null=True)  # Field name made lowercase.
    municipio_res = models.CharField(db_column='MUNICIPIO_RES',max_length=140, blank=True, null=True)  # Field name made lowercase.
    es_deudor = models.BooleanField(db_column='es_deudor', blank=True, null=True) # es deudor?
    vol_agua = models.IntegerField(db_column='VOLUMEN_A', blank=True, null=True) #m3 de agua
    tipo_cobro = models.IntegerField(db_column='TIPO_COBRO', blank=True, null=True) #4 tipos 

    def __str__(self):
        fila = "Cliente: " + str(self.id) + " - " + "Nombre: " + str(self.nombre)
        return fila
    
    def Nombre(self):
        return self.nombre + " " +self.apellidos
    
    def Domi(self):
        return self.direccion + "  CP." + str(self.cod_post) + " , " + self.municipio_res

    def EsDeudor(self):
        return self.es_deudor == True
    
    def calcular_pago_domestica(self):
        if self.vol_agua <= 10:
            return 104.57
        elif self.vol_agua <= 15:
            return self.vol_agua * 10.40
        elif self.vol_agua <= 30:
            return self.vol_agua * 13.47
        elif self.vol_agua <= 35:
            return self.vol_agua * 13.69
        elif self.vol_agua <= 50:
            return self.vol_agua * 20.86
        elif self.vol_agua <= 65:
            return self.vol_agua * 65.59
        elif self.vol_agua <= 75:
            return self.vol_agua * 66.74
        else:
            return self.vol_agua * 71.76

    def calcular_pago_social(self):
        if self.vol_agua <= 10:
            return 52.83
        elif self.vol_agua <= 15:
            return self.vol_agua * 5.28
        elif self.vol_agua <= 30:
            return self.vol_agua * 6.72
        else:
            return self.vol_agua * 6.72

    def calcular_pago_comercial(self):
        if self.vol_agua <= 10:
            return 513.89
        elif self.vol_agua <= 15:
            return self.vol_agua * 35.45
        elif self.vol_agua <= 20:
            return self.vol_agua * 35.78
        elif self.vol_agua <= 25:
            return self.vol_agua * 37.03
        elif self.vol_agua <= 35:
            return self.vol_agua * 37.71
        elif self.vol_agua <= 50:
            return self.vol_agua * 38.39
        elif self.vol_agua <= 75:
            return self.vol_agua * 39.06
        else:
            return self.vol_agua * 40.46

    def calcular_pago_especial(self):
        if self.vol_agua <= 10:
            return 651.13
        elif self.vol_agua <= 15:
            return self.vol_agua * 54.91
        elif self.vol_agua <= 20:
            return self.vol_agua * 55.37
        elif self.vol_agua <= 25:
            return self.vol_agua * 55.86
        elif self.vol_agua <= 35:
            return self.vol_agua * 56.85
        elif self.vol_agua <= 55:
            return self.vol_agua * 57.29
        elif self.vol_agua <= 75:
            return self.vol_agua * 60.30
        else:
            return self.vol_agua * 69.96
    
    def Deuda(self):
        if(self.tipo_cobro == 0):
            return self.calcular_pago_domestica()
        elif self.tipo_cobro == 1:
            return self.calcular_pago_social()
        elif self.tipo_cobro == 2:
            return self.calcular_pago_comercial()
        else:
            return self.calcular_pago_especial()
    
class User(AbstractUser):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE, blank=False, null=True)

    def Nombre(self):
        return self.cliente.Nombre() #filter(nombre="eduardo")
    def EsDeudor(self):
        return self.cliente.EsDeudor() #filter(nombre="eduardo")
    def Deuda(self):
        if self.cliente.EsDeudor():
            return int(self.cliente.Deuda())
        else:
            return 0
    def Domicilio(self):
        return self.cliente.Domi()