#!/usr/bin/env bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'

# Update sources
apt-get update

apt-get -y install zsh
sudo su - vagrant -c 'wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh 2>/dev/null 1>&2'
chsh -s /bin/zsh vagrant

cp /vagrant/.vagrant_provisioning/zshrc /home/vagrant/.zshrc

apt-get -y install ack-grep mercurial vim-nox
sudo su - vagrant -c 'curl http://j.mp/spf13-vim3 -L -o - | sh 2>/dev/null 1>&2'

apt-get -y install python-dev python-setuptools
sudo easy_install pip
sudo pip install virtualenv

apt-get -y install openjdk-7-jdk
curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.0.deb
dpkg -i elasticsearch-1.4.0.deb
sudo service elasticsearch start

apt-get -y install libjpeg-dev
apt-get -y install libldap-dev libsasl2-dev
apt-get -y install libxml2-dev libxslt1-dev
apt-get -y install poppler-utils
apt-get -y install redis-server

apt-get -y install adminer mercurial lynx
apt-get -y install mysql-client mysql-server libmysqlclient-dev
apt-get -y install postgresql postgresql-client postgresql-server-dev-all

# OCVE/CFEO MySQL database
mysql --password=password -e "CREATE DATABASE IF NOT EXISTS app_ocve_dev;"
mysql --password=password -e "CREATE USER 'app_ocve'@'localhost' IDENTIFIED BY 'password';"

tar -C /vagrant/.vagrant_provisioning -zxvf /vagrant/.vagrant_provisioning/ocve.sql.tar.gz
mysql --password=password app_ocve_dev < /vagrant/.vagrant_provisioning/ocve.sql
rm /vagrant/.vagrant_provisioning/ocve.sql

mysql --password=password -e "GRANT ALL ON app_ocve_dev.* TO 'app_ocve'@'localhost';"

# Catalogue Postgres database
sudo su - postgres -c "psql -c \"create user vagrant with superuser password 'vagrant';\""
sudo su - postgres -c "psql -c \"create user app_ocve password 'app_ocve';\""
sudo su - postgres -c "createdb app_ocve_dev -E UTF-8 -T template0 -O app_ocve"

tar -C /vagrant/.vagrant_provisioning -zxvf /vagrant/.vagrant_provisioning/aco.sql.tar.gz
sudo su - postgres -c "psql app_ocve_dev < /vagrant/.vagrant_provisioning/aco.sql"
rm /vagrant/.vagrant_provisioning/aco.sql

sudo su - postgres -c "psql app_ocve_dev -c \"grant all on database app_ocve_dev to app_ocve;\""

for tbl in `sudo su - postgres -c "psql -qAt -c \"select tablename from pg_tables where schemaname = 'public';\" app_ocve_dev"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_ocve;\" app_ocve_dev"
done

for tbl in `sudo su - postgres -c "psql -qAt -c \"select sequence_name from information_schema.sequences where sequence_schema = 'public';\" app_ocve_dev"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_ocve;\" app_ocve_dev"
done

for tbl in `sudo su - postgres -c "psql -qAt -c \"select table_name from information_schema.views where table_schema = 'public';\" app_ocve_dev"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_ocve;\" app_ocve_dev"
done

cp /vagrant/.vagrant_provisioning/local_settings.py /vagrant/chopin/settings/local.py

virtualenv /home/vagrant/venv
source /home/vagrant/venv/bin/activate
pip install -r /vagrant/requirements-dev.txt
python /vagrant/manage.py makemigrations --noinput
python /vagrant/manage.py migrate --noinput
python /vagrant/manage.py update_index

#sudo su - postgres -c "psql app_ocve_dev -c \"alter table wagtaildocs_document alter column file type varchar(256);\""

sudo chown -Rf vagrant /home/vagrant
sudo chown -Rf vagrant /vagrant
