this is the first version of readme document and the project is now under construction

1) start service(PostgreSQL):
sudo service postgresql start

2) entering PostgreSQL
sudo -u postgres psql

3) creating new database
CREATE DATABASE stock_db;
CREATE USER sunny_db WITH PASSWORD 'pwd';
GRANT ALL PRIVILEGES ON DATABASE stock_analysis TOsunny_db;

\l to show all db
\dt to show all tables in that db
\d 'table name' to show details of that table
\q to exit psql cmd line

4)setup git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

cd /home/sunny/workspace/autoTrade_insight
git init

git add .
git commit -m "Initial commit - project setup"

git remote add origin https://github.com/yourusername/yourrepository.git
git branch -M main
git push -u origin main

git status