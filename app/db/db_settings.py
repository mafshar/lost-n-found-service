DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lostnfound',
        'USER': 'admin',
        'PASSWORD': 'adminpassword',
        'HOST': 'localhost',
        'PORT': '',
     },
      'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lostnfound',
        'USER': 'admin',
        'PASSWORD': 'adminpassword',
        'HOST': 'localhost',
        'PORT': '',
    },
    'db1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lostnfound',
        'USER': 'admin',
        'PASSWORD': 'adminpassword',
        'HOST': 'localhost',
        'PORT': '',
    },
}

DATABASE_ROUTERS = ['lostnfound.routers.UserRouter']
