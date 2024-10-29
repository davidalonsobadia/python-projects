import click
from config import Config
from flask import current_app
from flask_mysqldb import MySQL


def create_mysql_db(database_name):
    mysql = MySQL(current_app)
    connection = mysql.connect
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database_name}')
    cursor.close()
    connection.close()

@click.command('create-mysql-db')
@click.option('--database-name', help='Enter the name of the database to create')
def create_mysql_db_command(database_name):
    """Create new database if it does not exists."""
    if database_name is None:
        database_name = Config.DB_NAME

    create_mysql_db(database_name)
    click.echo('Initialized the MYSQL database.')


def init_commands(app):
    app.cli.add_command(create_mysql_db_command)