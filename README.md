# Data science project
- Document here the project: chouwal
- Description: 2 weeks Data science project in order to apply technics learnt during Le Wagon bootcamp. The aim was to predict if a hourse would finish in the 3 first place or not. 
- Data Source: online database
- Team work: Lucas and Bastien as data engineers, Arnaud as team leader and Edouard as data scientist

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for chouwal in github.com/{group}. If your project is not set please add it:

Create a new project on github.com/{group}/chouwal
Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "chouwal"
git remote add origin git@github.com:{group}/chouwal.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
chouwal-run
```

# Install

Go to `https://github.com/{group}/chouwal` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/chouwal.git
cd chouwal
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
chouwal-run
```
