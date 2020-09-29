# Facebook Data Miner

[![BCH compliance](https://bettercodehub.com/edge/badge/tardigrde/facebook-data-miner?branch=master)](https://bettercodehub.com/)

Facebook-Data-Miner provides a set of tools that can help you analyze the data 
that Facebook has on you.

The vision is to support both data extraction, data analysis and data 
visualization capabilities through any of the interfaces.

All computation happens on your machine so no data gets sent to remote 
computers or third-parties.

## Prerequisites
As of now the package was only tested on Linux, however with `pipenv` 
it is should be easy to set the application up on Windows.

### Python

The application was tested on Debian 10 and Python v3.8.3.
You will need Python 3.8 (some features are used).

To download Python refer to the official Python 
[distribution page](https://www.python.org/getit/).

### Your Facebook data

This package works by analyzing your Facebook data, so you have to download it.

Please refer to the following 
[link](https://www.facebook.com/help/212802592074644) in order to do so. 

IMPORTANT NOTE: you have to set Facebook's language to English(US) for the 
time being you request your data. This change can of course be reverted later.

You will only need the zip file's absolute path later to use this software.

You have to change the `DATA_PATH` variable in the 
[configuration.yml](configuration.yml).

NOTE: `facebook-data-miner` will extract your zip file in the same directory. 
For this you may need several GBs of free space depending on the volume of the 
original data.

### This repository
Clone this repository by either using SSH:

```shell script
git clone git@github.com:tardigrde/facebook-data-miner.git
```

or HTTPS:

```shell script
git clone https://github.com/tardigrde/facebook-data-miner.git
```

### Dependecies

This project uses `pipenv` for dependency and virtual environment management.

Install it by typing:
```shell script
pip install --user pipenv
```

In the project root (where [Pipfile](Pipfile) is) run:

```shell script
pipenv install
```

Make sure you run the application in this environment.

## Usage

The app has both a CLI and an API. For now, API is the preferred way to 
run the app since there is no database yet, which would hold your facebook data
in memory. CLI works but it's slow.

### Jupyter notebook

I wrote two jupyter notebooks in order to showcase the capabilities and 
features of the API and CLI. The notebook contains lots of comments to 
help understand how the app is built, 
and what kind of information you can access, and how.

For this you have to start a `jupyter` server. 
As in the notebooks mentioned, you have to set the $PYTHONPATH env var 
before starting a jupyter server.

```shell script
export PYTHONPATH="$PWD"
```

Then type the following in your terminal if you want to use `jupyer notebook`:

```shell script
jupyer notebook
```

or for `jupyter lab`:

```bash
jupyter lab
```

Select [notebooks/API.ipynb](notebooks/API.ipynb) 
(or [notebooks/CLI.ipynb](notebooks/CLI.ipynb)) and start executing the cells. 

### The API
As in the notebook already described, the entrypoint is 
[miner/app.py](miner/app.py)'s `App` class. For now the docstring is the only
documentation.

Call it from a script (after you set the data path) like:
```python
from miner.app import App
app = App()
```

### The CLI

The command-line interface has a lot of depth, as you are showed in
 [notebooks/CLI.ipynb](notebooks/CLI.ipynb), but it is slow, 
 because the data that gets read in does not stay in RAM.

For running the CLI:

```shell script
export PYTHONPATH="$PWD"
python ./miner/app.py --help
```

## Contribution

Help is more than welcome. It is still a long way to go until v1.0.0

Ideas are welcome too. Feel free to open a new issue.
