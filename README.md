# Facebook Data Miner

[![BCH compliance](https://bettercodehub.com/edge/badge/tardigrde/facebook-data-miner?branch=master)](https://bettercodehub.com/)

This repository provides a set of tools integrated into one conscise Command-Line Interface that can help you analyze the data that Facebook has on you.

The vision is to support both data extraction, data analysis and data visualization capabilities through any of the interfaces.

All computation happens on your machine so no data gets sent to remote computers or third-parties.

**NOTE:** The codebase is under development.

Features will be added gradually, starting with basic analysis of the messages.

## Prerequisites

### Python

You will need Python for running this piece of software.

The application was tested on Debian 10 and Python v3.8.3.

To download Python refer to the official Python [distribution page](https://www.python.org/getit/).

### Your Facebook data

This package works by analyzing your Facebook data, so you have to download it.

Please refer to the following [link](https://www.facebook.com/help/212802592074644) in order to do so. IMPORTANT NOTE: you have to set Facebook's language to English(US) for the time being you request your data. This change can of course be reverted later.

You will only need the zip file's absolute path later to use this software. NOTE: `fb-data-miner` will extract your zip file in the same directory. For this you may need several GBs of free space depending on the volume of the data.

### This repository
Clone this repository by either using SSH:

```bash
git clone git@github.com:tardigrde/facebook-data-miner.git
```

or HTTPS:

```bash
git clone https://github.com/tardigrde/facebook-data-miner.git
```

### Dependecies

It is preferred to create a new Python virtual environment or conda environment to install the dependecies and run the application in.

After you have created and activated the environment install the dependecies by running:

```bash
pip install -r requirements.txt
```

Make sure you run the application in this environment.

## Usage
### Jupyter notebook

I wrote a jupyter notebook in order to showcase the capabilities and features of the application. For now, this is the preferred way to run the app.
The notebook contains lots of comments to help understand how the app is built, and what kind of information you can access, and how.

For this you have to start a ipyhton server. Type the following in your terminal if you want to use `jupyer-notebook`:

```bash
jupyer-notebook
```

or for `jupyter lab`:

```bash
jupyter lab
```

Select `facebook_data_analyzer.ipynb` and start executing the cells. You will only have to change on thing in the notebook (in the first code cell), and that is the `path` to the data zip file.

### The Command-Line Interface

The command line interface is not too powerful yet, but will be improved as new features will be added.

For running the CLI:

```bash
export PYTHONPATH="$PWD"
python ./miner/app.py --help
```

## Contribution

Help is more than welcome. If somebody feel the urge to contribute, I would share my plans with them.

Ideas are welcome too. Feel free to open a new issue.
