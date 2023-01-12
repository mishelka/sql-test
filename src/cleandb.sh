SET PGCLIENTENCODING=utf-8
chcp 65001
psql -U postgres < obce.sql
pip3 install psycopg2