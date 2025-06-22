# Sistema de Ventas

Este proyecto es una aplicación web basada en Django que permite gestionar vendedores, registrar ventas y calcular comisiones basadas en reglas predefinidas. La aplicación implementa el patrón **Model-View-Template (MVT)** para mantener una estructura modular y escalable.

---

## Características

- **Registro de ventas**: Permite registrar ventas asociadas a un vendedor y fecha específica.
- **Cálculo de comisiones**: Calcula las comisiones y bonos de vendedores según un periodo seleccionado.
- **Soporte para múltiples vendedores**: Realiza cálculos para un vendedor específico o para todos los vendedores en conjunto.
- **Interfaz moderna**: Utiliza Bootstrap 5 para un diseño limpio y responsivo.

---

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- Django 5.2.3
- Bootstrap (vía CDN)

### Pasos para instalar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/sistema-de-ventas.git
   cd sistema-de-ventas

2. Crea un entorno Virtual e Instalalo:
    ```bash
    python -m venv venv
    source venv/bin/activate   # En Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. Configura la base de datos:
    ```bash
    python manage.py migrate

4. Ejecuta el servidor local:
    ```bash
    python manage.py runserver

5. Accede a la aplicacion en el navegador:
    ```bash
    http://127.0.0.1:8000/

# Uso
Registro de ventas
Ve a la página de Registrar Venta desde la barra de navegación.

Selecciona un vendedor, ingresa la cantidad y la fecha de la venta.

Haz clic en Registrar Venta.

Cálculo de comisiones
Ve a la página de Calcular Comisiones desde la barra de navegación.

Selecciona un vendedor (o deja el campo vacío para calcular para todos).

Define un rango de fechas y haz clic en Calcular.

Los resultados se muestran en una tabla con las ventas totales y bonos por vendedor.

# Estructura del Proyecto
sistema-de-ventas/
├── gestorventas/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── base.html
│   │   ├── calcular_bono.html
│   │   ├── index.html
│   │   ├── registrar_venta.html
│   │   ├── ventas_exito.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
├── manage.py
└── requirements.txt

# Modelos
    ## VendedorModel

        Campos:

        vendedorId: Identificador único (clave primaria).

        nombreVendedor: Nombre del vendedor.

        apellidoVendedor: Apellido del vendedor.

    ## VentasModel

        Campos:

        ventaId: Identificador único (clave primaria).

        fechaVenta: Fecha de la venta.

        cantidadVenta: Monto de la venta.

        vendedorId: Relación con el modelo VendedorModel.

    ## ReglasModel
        Campos:

        reglaId: Identificador único (clave primaria).

        metaVenta: Meta de ventas para calcular comisión.

        cantidadComision: Porcentaje de comisión.

# Plantillas

    1. base.html: Plantilla base para compartir el diseño del header y footer.

    2. index.html: Página principal del sistema.

    3. calcular_bono.html: Cálculo de comisiones y visualización de resultados.

    4. registrar_venta.html: Formulario para registrar nuevas ventas.

    5. ventas_exito.html: Mensaje de confirmación tras registrar una venta.

# Fuentes utilizadas para comprender el proyecto

    Query Filter Events By Date - Django Wednesdays #36
    https://www.youtube.com/watch?v=4AnwvUJGJzw

    Django ORM - SQL Insert - Working with datetime fields and foreign keys
    https://www.youtube.com/watch?v=7dV3hyql8x0

    How do I filter query objects by date range in Django?
    https://www.youtube.com/watch?v=Mx8ABgqfL3Q

    Django Official Documentation
    https://docs.djangoproject.com/en/5.2/

    Curso Práctico de Django: Desarrollo Web Backend con Python
    https://www.udemy.com/course/curso-django-2-practico-desarrollo-web-python-3/?srsltid=AfmBOopw3bxpo7Ma98QNg9s-XQLWiCCCcu4-ZMJxT6vrUJUGSvBr-Eey

# Contacto
    mateo.jaramillo.costa@udla.edu.ec