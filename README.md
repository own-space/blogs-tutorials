# Virtual environment for python
python3 -m venv <venv-name>
# Connecting to database hosted in AWS
psql -h database-1.cicwaimxo6tr.eu-west-2.rds.amazonaws.com -p 5432 -d postgres -U postgres

# Creating new database schema into postgresql database for my app
CREATE DATABASE blogappdb_v1;
CREATE USER blogapper WITH ENCRYPTED PASSWORD 'passwords';
GRANT ALL PRIVILEGES ON DATABASE blogappdb_v1 to blogapper;

# grunt contrib sass (used scss for styling elements)
http://ryanchristiani.com/getting-started-with-grunt-and-sass/
    sudo npm install -g grunt-cli
        Option 1:
        Using the commandline cd into your projects root directory. If you have an existing project and package.json you can simply run npm install and all the dependencies will be installed.

        Option 2:
        Lets assume you are starting fresh, running npm init on the commandline from your project root will set up only the package.json file for you.

        Option: 3
        Or you can set up your own package.json file. Here is a simple example:
        node_modules will generate after run grunt command
    Run below commands in project directory, this will generate node_modules/ package.json and package-lock.json files.
    ```sudo npm install grunt --save-dev```
    sudo npm install grunt-contrib-sass --save-dev
    sudo npm install grunt-contrib-watch --save-dev
    run ```grunt``` to start and save the scss files into css
This procedure would convert SCSS files to CSS files and store generated CSS files to folder mentioned at **grunt.initConfig** in Gruntfile.js 

Now, we collect media data and packaged CSS shipped with installed django packages using command ```python3 manage.py collectstatic```
This copies data to static folder as set **STATIC_ROOT** in settings.py file 


# django-github-cicd
The project contains standard Django applications customised to use with GitHub Actions. GitHub Actions used to deploy application to AWS Instance, using Terraform.



|  Tool  |   Version    |
|--------|--------------|
| Python | Python 3.8.9 |

Workflows uses below secrets while provisioning infrastructure

| Secret Name | Its Use |
|-------------|---------|
| APP_SECRET  |         |
| AWS_ACCESS_KEY_ID|         |
| AWS_REGION|         |
| AWS_SECRET_ACCESS_KEY|         |
| DB_APP_USER|         |
| DB_AUTH|         |
| DB_HOST|         |
| DB_NAME|         |
| DB_PORT|         |
| DB_PWD|         |
| NEW_IMAGE|         |
| TF_API_TOKEN|         |
