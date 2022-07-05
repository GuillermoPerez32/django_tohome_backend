1-instalar la libreria para crear el entorno virtual entorno virtual con ```pip install virtualenv```
2-moverse a donde tengas el proyecto y adentro...
3-Crear entorno virtual con ````virtualenv venv```
4-activar el entorno virtual. tienes q hacerlo cada vez q quieras ejecutar el proyecto
4.1-```& venv/Scripts/Activate.ps1``` para activar el entorno virtual en windows
4.1-```source venv/bin/activate``` para activar el entorno virtual en linux
Debe quedarte la consola parecido a ```(venv) PS D:\Proyectos\toHome\```
5-Ejecutas migraciones con ```python manage.py migrate```
6-Ejecutas migraciones sincronizando a la base de datos con ```python manage.py migrate --run-syncdb```
7-Crearte un superuser con ```python manage.py createsuperuser```
8-Correr la aplicacion con ```python manage.py runserver [puerto]```,estara corriendo en el puerto 8000 por defect
