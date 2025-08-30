# market-edge-platform



### Dougs app todos. 
[x] 1.  upgrade to postgres 17
2. For blog, add post/Review model
3. Add stocks to the portfolios
4. Add integration to FMP for getting stock prices
[x] 5. Unit tests
[] 6. Secure SMTP and different email provider
[] 7. Logging




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
pyenv install 3.11.13
```

3. Create (and activate as needed) the dedicated virtual environment:
```
pyenv virtualenv 3.11.13 django-portfolio-app-api
pyenv activate django-portfolio-app-api
```

4. Now that you have created your named virtual environment (django-portfolio-app-api etc), set the local python environment:
```
pyenv local django-portfolio-app-api
```



5.  Install Django and some other basic depedencies to get started:
```
pip install Django==5.2.2
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

3. To run the test suite

```
    python manage.py test
    // For single tests.
    python manage.py test portfolios.tests.test_web
```



# Do you love to get postgres setup for your local python environment?  
# if so, follow the following to get going

1.  Install via homebrew
```
brew services start postgresql@17
psql postgres
```

2. Now log in
```
psql -U sqlmigrations -d postgres
```

3. Create the DB for your app, and make sure to include this in an .env file out of source control
CREATE DATABASE <db_name>;

4. Log in again
```
psql -U sqlmigrations -d <db_name>
```

5. Create the user role for your Django app
```
CREATE ROLE <my_user> WITH LOGIN;
```

You may also list users to verify its there
```
\du to list users
```

6. Its important your user has the priviledges it needs to operate in this new table
```
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES
    IN SCHEMA public
    TO <my_user>;
-- Enable this for all new tables.
ALTER DEFAULT PRIVILEGES
    GRANT SELECT, INSERT, UPDATE, DELETE
    ON TABLES
    TO <my_user>;
-- Allow our user to use SEQUENCES.
-- It's required to insert data with auto-incrementing primary keys for instance.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO <my_user>;
ALTER DEFAULT PRIVILEGES
    GRANT USAGE, SELECT
    ON SEQUENCES
    TO <my_user>;
```

7. 
```
REVOKE GRANT OPTION
    FOR ALL PRIVILEGES
    ON ALL TABLES
    IN SCHEMA public
    FROM <my_user>;
ALTER DEFAULT PRIVILEGES
    REVOKE GRANT OPTION
    FOR ALL PRIVILEGES
    ON TABLES
    FROM <my_user>;
```

8. You may now log in to your new DB in the console.
```
psql -U postgres -d <db_name>
```