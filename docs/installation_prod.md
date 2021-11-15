## Installation guide for production systems

This guide will focus on Debian/Ubuntu-like systems - however, it works very similar on e.g. Fedora and friends.

### Package requirements:
 * python3
 * python3-pip
 * virtualenvwrapper
 * gettext
 * git
 * curl
 * nodejs ([in an up-to-date version](https://github.com/nodesource/distributions/blob/master/README.md))
 * nginx / apache webserver
 * optionally: a database like postgresql / mariadb

### Step-by-step setup

#### Create user
Create and switch to user (as `root` or using `sudo`)

```
adduser kosmo
su kosmo
cd
```

#### Get the code
```
git clone https://github.com/liqd/a4-kosmo.git
cd a4-kosmo
git checkout release
```

#### Create and launch virtual environment
```
mkvirtualenv --python=/usr/bin/python3 kosmo
```

Note: you won't need the `--python` part when using a recent distribution.

#### Install dependencies and build static optimized JS code
```
npm install
npm run build:prod
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.build
python manage.py compilemessages
python manage.py collectstatic
```

#### Static configuration (`local.py`)

Create a config file at `~/a4-kosmo/adhocracy-plus/config/settings/local.py`

See the [django-documentation](https://docs.djangoproject.com/en/2.2/ref/settings/) for a comprehensive list of settings and `config/settings/base.py` for pre-configured ones. The settings you will most likely want to set are:

```
# replace 'your.domain' with your desired domain
WAGTAILADMIN_BASE_URL = 'https://your.domain'
ALLOWED_HOSTS = [u'your.domain', u'localhost']

# database config - we recommend postgresql for production purposes
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'kosmo-test-database',
  }
}

# forward outgoing emails to a local email proxy
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='127.0.0.1'

# folder for user-uploads, directly served from the webserver (see nginx example below). Must be created manually.
MEDIA_ROOT='/home/kosmo/kosmo-media'

# replace the value below with some random value
SECRET_KEY = u'SOMESECRETKEY'

# some basic security settings for serving the website over https - see django docu
CSRF_COOKIE_SECURE=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True

FILE_UPLOAD_PERMISSIONS = 0o644
```

#### Populate database

This will create all required tables via so called **migrations**

```
python manage.py migrate
```

#### Test run

Try starting the server:

```
export DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.production
python manage.py runserver
```

From another terminal on the same server:

```
curl localhost:8000
```

You should now get valid HTML output.

Cancel the server after testing via `ctrl`+`c`

### Run the server as system daemon

In order to start up the software as a regular system daemon, similar to a database or webserver, we need to create unit files.

`/etc/systemd/system/kosmo.service`:

```
[Unit]
Description=kosmo server
After=network.target

[Service]
User=kosmo
WorkingDirectory=/home/kosmo/a4-kosmo
ExecStart=/home/kosmo/.virtualenvs/kosmo/bin/gunicorn -e DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.production --workers 4 --threads 2 -b 127.0.0.1:8000 -n kosmo adhocracy-plus.config.wsgi
Restart=always
RestartSec=3
StandardOutput=append:/var/log/kosmo/kosmo.log
StandardError=inherit

[Install]
WantedBy=default.target
```

`/etc/systemd/system/kosmo-background-task.service`:

```
[Unit]
Description=kosmo background task
After=network.target

[Service]
User=kosmo
WorkingDirectory=/home/kosmo/a4-kosmo
ExecStart=/home/kosmo/.virtualenvs/kosmo/bin/python manage.py process_tasks --settings adhocracy-plus.config.settings.production --sleep 5
Restart=always
RestartSec=3
StandardOutput=append:/var/log/kosmo/kosmo-background-task.log
StandardError=inherit

[Install]
WantedBy=default.target
```

This will log all output to files in `/var/log/kosmo/`. You will also need to create that folder before starting the service (as `root` or using `sudo`):

```
mkdir /var/log/kosmo
```

Load and start units (as `root` or using `sudo`):

```
systemctl daemon-reload
systemctl start kosmo
systemctl start kosmo-background-task
```

Enable autostart on boot:

```
systemctl enable kosmo
systemctl enable kosmo-background-task
```

### Setting up a proxy webserver

Finally, we need to set up a proxy webserver which handles the communication with the outside world. The following example is a simple config for `nginx`:

```
server {
  listen 80;
  listen [::]:80;

  # for using https - see nginx docu
  #listen 443 ssl http2;
  #listen [::]:443 ssl http2;

  server_name your.domain;

  # forward traffic to kosmo
  location / {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:8000;
  }

  # serve media files directly, without going through kosmo.
  # See MEDIA_ROOT in local.py
  location /media {
    alias /home/kosmo/kosmo-media;
  }

  # max upload size for images and documents
  client_max_body_size 20m;
}

```

The website should now be reachable

### Admin user and first organization

You can now continue setting up the website in the `django-admin` configuration page. Please also see the [manual](https://manual.adhocracy.plus/) for a more comprehensive documentation.

#### Create initial admin user

```
su kosmo
cd ~/a4-kosmo
workon kosmo
python manage.py createsuperuser
```

#### Django-admin

Visit `http[s]://your.domain/django-admin` and log in with the user you just created.

#### Domain settings

In the `sites` (german: `Websites`) section, change the domain name of the existing site to `your.domain`

#### First organisation

In the `Organisations` section, add a new organization. For the moment, all you need is setting the name and adding you user to the `Initiators`.

You can now visit `http[s]://your.domain/` and select the organization from the user dropdown menu - it will bring you to the `dashboard`. See the [manual](https://manual.adhocracy.plus/).

#### Landing page

The landing page is managed via [wagtail](https://wagtail.io/). You can find the settings at `http[s]://your.domain/admin`.

### Updating

#### Stop server

```
systemctl stop kosmo
systemctl stop kosmo-background-task
```

#### Switch to user

```
su kosmo
cd ~/a4-kosmo
```

####  Enable virtual environment

```
workon kosmo
```

#### Update the code

```
git pull
```

#### Cleanup old static files

```
rm -rf static/*
```

#### Update dependencies and rebuild static optimized JS code

```
npm install
npm run build:prod
pip install --upgrade -r requirements.txt
export DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.build
python manage.py compilemessages
python manage.py collectstatic
```

#### Update Database

```
python manage.py migrate
```

#### Try starting the server

```
export DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.production
python manage.py runserver
```

#### Restart server (as `root` or using `sudo`)

```
systemctl start kosmo
systemctl start kosmo-background-task
```
