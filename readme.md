# Getting a local python environment set up using pyenv

We reccomend setting up a virtual environment with a specific version of python dedicated to this project.  At the time of creation we opted to use the latest and greatest with Django 4.2 and Python 3.11.  This will walk you through getting python and Django set up assuming you have not pulled down this source code yet.

1. using homebrew, install pyenv and virtualenv to manage python installations and virutal environments:
```
brew install pyenv
brew install virtualenv
```

2. Install the version of python for your project.  First fetch the list of available installs by running:
```
pyenv install --list
```

Proceeed with version 3.11 installation:
```
pyenv install 3.11.0
```

3. Create (and activate as needed) the dedicated virtual environment:
```
pyenv virtualenv 3.11.0 django-mkt-app
pyenv activate django-mkt-app
```

4. Now that you have created your named virtual environment (django-mkt-app etc), set the local python environment:
```
pyenv local django-mkt-app
```

5.  Install Django and some other basic depedencies to get started:
```
pip install Django==4.2.4
pip install numpy pandas matplotlib
```

6. If you are using VS code, open a file and on the bottom right of the window, select the python interpreter.  You should be able to find an auto generated list
of python runtimes to use.  Find "django-mkt-app" (python 3.11.0) or whatever you named your virtual environment.


# Testing

1. Install model bakery - this will help with object creation especially for the large objects with a large number of fields in them. 

```
pip install model_bakery
```

2.  Everything about python is easy except the testing.  Use this debugger on the line you want your test to pause.

```
import pdb; pdb.set_trace()
```

