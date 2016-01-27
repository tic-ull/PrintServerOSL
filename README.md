#Printer Server

##Pasos para despliegue

* Instalar VirtualEnv en el server y crear el entorno donde deseemos:

```
$ sudo apt-get install python-virtualenv
$ sudo virtualenv /opt/imp_serv
```

* Instalar Django dentro del VirtualEnv recién creado:

```
$ cd /opt/imp_serv
$ source bin/activate
$ sudo pip install django
```

* Creamos la carpeta donde almacenaremos el proyecto:

```
$ sudo mkdir imp_serv
$ cd imp_serv
```

* Clonar repositorio desde Bitbucket:

```
$ sudo apt-get install git
$ sudo git clone https://<user>@bitbucket.org/igeko/printerserver.git .
```

* Instalar depencencias con Pip:

```
sudo pip install django-filter
sudo pip install djangorestframework
sudo pip install netaddr
sudo pip install pypdf2
sudo pip install django_reset
```

* Crear las migraciones y las tablas de la base de datos:

```
$ sudo python manage.py makemigrations
$ sudo python manage.py migrate
```

* Cuando se vaya a poner el producción el servicio, modificar las partes de el fichero 'settings.py' de la siguiente manera:

```
DEBUG = False
ALLOWED_HOSTS = ['*']
.
.
.
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
```

* Crear carpeta para ficheros estáticos en el mismo directorio que 'manage.py' y generarlos allí:

```
$ sudo mkdir static
$ sudo python manage.py collectstatic
```

* Crear dominio en Nginx:

```
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/<nombre_del_dominio>
```

* Modificar el fichero recién creado de manera que contenga el siguiente código:

```
server {
        listen 80;
        listen [::]:80;

        server_name <nombre_del_dominio>;

        access_log off;

        location /static/ {
                root /opt/imp_serv/imp_serv/;
                autoindex off;
        }

        location / {
                #try_files $uri $uri/ /index.php?q=$uri&$args;
                proxy_set_header Host $host;
                proxy_pass http://<nombre_del_dominio>:8001;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        

        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
                root /usr/share/nginx/html;
        }

}
```

* Activamos nuestro sitio y reiniciamos el servicio de Nginx:

```
$ sudo ln -s /etc/nginx/sites-available/<nombre_del_dominio> /etc/nginx/sites-enabled/
$ sudo service nginx restart
```

* Nos dirigimos ahora a nuestra carpeta del proyecto y entramos en nuestro entorno virtual, si no lo estamos ya, para instalar Gunicorn:

```
$ cd /opt/imp_serv/imp_serv
$ source ../bin/activate
$ sudo pip install gunicorn
```

* Por último ejecutar el comando necesario con Gunicorn para poner la página a funcionar:

```
$ gunicorn SWP.wsgi:application --bind <nombre_del_dominio>:8001
```
