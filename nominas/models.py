from django.db import models

# Create your models here.
# Create your models here.
class Regiones(models.Model):
    region_id = models.AutoField(primary_key=True)
    nombre_region = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'regiones'

class Paises(models.Model):
    pais_id = models.AutoField(primary_key=True)
    nombre_pais = models.CharField(max_length=100)
    region = models.ForeignKey('Regiones', on_delete=models.CASCADE, db_column='region_id')
    
    class Meta:
        db_table = 'paises' 

class Ubicaciones(models.Model):
    ubicacion_id = models.AutoField(primary_key=True)
    direccion_calle = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.ForeignKey('Paises', on_delete=models.CASCADE, db_column='pais_id')
    
    class Meta:
        db_table = 'ubicaciones'

class Departamentos(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=100)
    gerente = models.ForeignKey('Empleados', on_delete=models.CASCADE, db_column='gerente_id')
    ubicacion = models.ForeignKey('Ubicaciones', on_delete=models.CASCADE, db_column='ubicacion_id')  
    
    class Meta:
        db_table = 'departamentos'

class Puestos(models.Model):
    puesto_id = models.CharField(primary_key=True, max_length=10)
    titulo_puesto = models.CharField(max_length=100)
    salario_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    salario_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'puestos'



class Empleados(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.IntegerField()
    telefono = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    puesto = models.ForeignKey(Puestos, on_delete=models.CASCADE, null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_comision = models.DecimalField(max_digits=10, decimal_places=2)
    gerente = models.ForeignKey('Empleados', on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.ForeignKey('Departamentos', on_delete=models.CASCADE, null=True, blank=True) 

    
    
    class Meta:
        db_table = 'empleados'
    
    