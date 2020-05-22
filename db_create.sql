-- to run 
-- psql -d postgres -f db_create.sql
create user spyify_user with encrypted password 'spyify';

CREATE DATABASE spyify;
grant all privileges on database spotz to spyify_user;