sleep 30
sudo yum update -y
sleep 10
# install Ruby 2.4 and Sass 3.4
sudo yum install -y ruby ruby-devel ruby-rdoc ruby-ri ruby-irb ruby-shadow gcc gcc-c++ libxml2-devel libxslt-devel
sudo yum install -y ruby-full ruby-devel ruby-rdoc ruby-ri ruby-irb ruby-shadow gcc gcc-c++ libxml2-devel libxslt-devel
sudo amazon-linux-extras install ruby2.6 -y
gem install sass
sleep 1

# install nginx
sudo amazon-linux-extras install nginx1 -y
sleep 1
# update PATH 
export PATH=$PATH:/usr/local/bin
echo "export PATH=$PATH:/usr/local/bin" >> ~/.bash_profile
sleep 1
source ~/.bash_profile
sleep 10
# https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html
echo "installing npm (on Amazon linux)"
cd $HOME
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
. ~/.nvm/nvm.sh
nvm install --lts
node -e "console.log('Running Node.js ' + process.version)"

echo "installing git"
sudo yum install git -y
sudo yum install python3-pip -y
# sudo yum install libpq-dev python-dev -y
# update pip3 to latest version
python3 -m pip install --upgrade pip

# Below lines are needed to add private ssh key for github, allows cloning private repos
# mkdir -p ~/.ssh
# touch /root/.ssh/id_rsa
# cat /tmp/superrirya_github >> ~/.ssh/id_rsa

# chmod +x /tmp/mkssh.sh
# /tmp/mkssh.sh

# git config --global user.name "user"
# git config --global user.email "user@hotmail.com"
# eval $(ssh-agent -s)
# chmod 600 ~/.ssh/id_rsa 
# ssh-add ~/.ssh/id_rsa
# ssh-keyscan github.com >> ~/.ssh/known_hosts
#rm -f /tmp/superrirya_github
pip3 install gunicorn
pip3 install psycopg2-binary
pip3 install Pillow

sleep 10
git clone --branch ${github_branch} https://github.com/own-space/blogs-tutorials.git /src
git clone --branch ${github_branch} ${GITHUB_REPO} /tmp/src
me=`whoami`
sudo chown -Rf $me /src

#pip3 install --upgrade pip
pip3 install -r /tmp/requirements.txt

# install grunt cli 
cd /src/application
npm install -g grunt-cli
npm install grunt --save-dev
npm install grunt-contrib-sass --save-dev
npm install grunt-contrib-watch --save-dev
# npm install --save node-sass grunt-sass
grunt

#setting APP_DIR
export APP_DIR=/src/app
echo "export APP_DIR=/src/application" >> ~/.bash_profile
echo "export APP_DIR=/src/application" >> /home/ec2-user/.bash_profile

# script to create unique id for app secret key
echo 'import uuid' > /tmp/generate_secret.py
echo 'print(uuid.uuid4())' >> /tmp/generate_secret.py
secret_key=`python3 /tmp/generate_secret.py`
echo "NEW_APP_SECRET_KEY='${secret_key}'" | tee /src/application/django_app/env

touch /src/application/django_app/.env
cat << EOF > /src/application/django_app/.env
DB_PASSWORD="${DB_PWD}"
DJANGO_SECRET_KEY="${APP_SECRET}"
SECRET_KEY="${secret_key}"
DB_USER="${DB_APP_USER}"
DB_NAME="${DB_NAME}"
DB_PWD="${DB_PWD}"
DB_HOST="${DB_HOST}"
DB_PORT="${DB_PORT}"
EOF

touch /src/application/django_app/env
cat << EOF > /src/application/django_app/env
DB_PASSWORD="${DB_PWD}"
DJANGO_SECRET_KEY="${APP_SECRET}"
DB_USER="${DB_APP_USER}"
DB_NAME="${DB_NAME}"
DB_PWD="${DB_PWD}"
DB_HOST="${DB_HOST}"
DB_PORT="${DB_PORT}"
EOF

python3 /src/application/manage.py makemigrations
python3 /src/application/manage.py migrate

# setup nginx and gunicorn
cp /tmp/nginx_app.conf /etc/nginx/conf.d/app.conf
pip3 install gunicorn
cp /src/application/appmd.service /etc/systemd/system/djapp.service
systemctl start djapp
sudo chown -Rf ec2-user /src

# update settings file to allow hosts from other domains
sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \[\"*\"\]/g' /src/application/django_app/settings.py

# setup directory structure required for application to run
mkdir -p /src/application/log && chmod -Rf 777 /src/application/log
mkdir -p /src/application/run && chmod -Rf 777 /src/application/run
sudo chkconfig nginx on
sudo chkconfig djapp on
