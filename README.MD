# Laborator.io #

This is a Laboratory Manager, to install its dependencies please try to use the
virtualenv tool, installing it with pip and installing required dependencies
from the `requirements.txt` file contained within this repository.

This project uses Python 3. Be sure to have it installed correctly.

### Linux ###

To install dependencies:

```bash
alias python='python3' # to ensure you will use python 3

python -m ensurepip --user # run this with python 3 please

python -m pip install -U pip --user # to update pip

python -m pip install -U virtualenv --user # to install/update virtualenv

python -m virtualenv venv # to create a virtualenv named venv

. ./venv/bin/activate # to activate the venv virtualenv

pip install -r requirements.txt # to install dependencies
```

Before running be sure to run the `. ./venv/bin/activate` once to be on the
virtualenv, that can be noticed with the `(venv)` before the $ or # sign

To run in dev mode:

```bash
./dev.sh
```

To run in production mode:
```bash
./run.sh
```

### Windows ###

To install dependencies:

```batch
python -m ensurepip --user # run this with python 3 please

python -m pip install -U pip --user # to update pip

python -m pip install -U virtualenv --user # to install/update virtualenv

python -m virtualenv venv # to create a virtualenv named venv

.\venv\Scripts\activate.bat # to activate the venv virtualenv

pip install -r requirements.txt # to install dependencies
```

Before running be sure to run the `.\venv\Scripts\activate.bat` once to be on
the virtualenv, that can be noticed with the `(venv)` before the $ or # sign

To run in dev mode:
```batch
dev.bat
```
