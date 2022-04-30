# MausCrawler
This is a proof-of-concept project to demonstrate the systematically harvesting of webdata. The project was inspired by a zoom meeting. The implementation was done on a boring TV evening :smile:

Therefore this project does not crawl the full data set available, but is limited to a demo subset - just enough to proof the concept. However, considerations are given for easy and modular extensions to also crawl similar web databases. Just use or modify to your private needs but only to gather a private backup of data.

## Installation instructions

### 1. Get a Python installation
Get yourself a working Python3 environment:
Windows users may refer to and install a python environment according to the [Anaconda Python Distribution](https://www.anaconda.com/products/distribution) installation guide. Most Linux users should have python3 installed anyway:
```bash
# Example on Ubuntu Linux:
sudo apt install python3 python3-pip python3-venv
```

### 2. Get a local working copy of this git directory
Use git to get or update your copy of this Repository. 
```bash
git clone https://github.com/Deichgeist/MausCrawler.git
```
If you do not have a git installed on you local machine, download yourself a copy of the package as a zip file. (see download link above)


### 3. Create a virtual python environment 
I recommend to create a local python environment inside your local workspace repository:
```bash
# Create the environment:
python3 -m venv venv

# Activate the virtual environment:
source venv/bin/activate
```
Install the required python packages:
```bash
python3 -m pip install -r requirements.txt
```

## Usage: Ready to rumble:
Now you are ready to go. Just start the beast: 
```bash
python3 crawl.py
```
