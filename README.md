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

To run locally:

```bash
cd /path/to/lost-n-found-service
workon largescale
python ./app/manage.py migrate
python ./app/manage.py runserver
```

point your browser to: localhost:8000
