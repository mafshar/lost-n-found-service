# lost-n-found-service
Web-based Lost &amp; Found Service

To run:

make sure you have virtual env and virtual env wrapper; if not, type:

```bash
pip install virtualenv virtualenvwrapper
```

and then put these two lines in your `.bashrc` or `.bash_profile`:

```bash
# Virtualenv/VirtualenvWrapper
source /usr/local/bin/virtualenvwrapper.sh
```

clone the repo in your working directory and type:

```bash
. setup.sh
```

NOTE: if python starts to make your terminal session act strangely, type this command in terminal (assuming you have macports installed):

```bash
sudo port selfupdate && sudo port clean python27 && sudo port install python27 +readline
```

First, download mysql from: http://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.16-osx10.11-x86_64.dmg

Screenshot password given by the installer.
Start mysql server by going to your System Preferences and starting mysql

Then run commands:

```bash
mysql -u root -p #it'll prompt for password, type in the password given during installation
```

```mysql
SET PASSWORD FOR root@'localhost' = PASSWORD('<YourPreferredPasswordHere>');
#Set a short & sweet root password, cause you'll be using it quite a bit

CREATE DATABASE lostnfound;


GRANT ALL PRIVILEGES ON lostnfound.* to admin@'localhost' IDENTIFIED BY 'adminpassword';
#this is not your preferred password - please use adminpassword as the actual password for consistency between the four of us
```

Now, download and install Docker:
https://docs.docker.com/docker-for-mac/

Make sure to install the STABLE channel.

After installation, make sure the Docker daemon is running, and then run:

```bash
cd lost-n-found-service/app/db
source ./run_docker_dbs.sh
start_docker_dbs
./install_db.sh #This will prompt you for your root passwords you set up earlier. If it gives you an error saying 'lostnfound' db already exists, that's a good thing! Continue to the next steps.
```
To run locally:

```bash
cd /path/to/lost-n-found-service
workon largescale
python ./app/manage.py makemigrations
python ./app/manage.py migrate
python ./app/manage.py migrate --database=auth_db
python ./app/manage.py migrate --database=db1
python ./app/manage.py runserver
```

point your browser to `localhost:8000`
