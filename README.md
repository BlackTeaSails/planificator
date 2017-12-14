# Planificator 3000
Un planificador de tareas para resolver el problema de next release features:
* Podemos añadir Clientes y autorizar planificadores.
* Añadir y gestionar proyectos con sus requisitos.
* Dar peso a los requisitos segun el valor que le de cada uno de los clientes.

## Instrucciones para desarrollo

* Crea las migraciones a partir de los cambios en los modelos.

`python manage.py makemigrations`

* Migrate crea la base de datos a partir de las migraciones, si habeis tocado modelos, hace falta crear las migraciones primero.

`python manage.py migrate` 

* Crea un usuario con permisos para tocar la base de datos a través del modulo admin (no estan configurados por que no usamos modelos personalizados aun, solo estan los usuarios).

`python manage.py createsuperuser`

* Arranca el servidor de pruebas.

`python manage.py runserver`
