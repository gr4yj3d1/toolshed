#!/usr/bin/env python3
import os
import sys

import dotenv


def yesno(prompt, default=False):
    if not sys.stdin.isatty():
        return default
    yes = {'yes', 'y', 'ye'}
    no = {'no', 'n'}

    if default:
        yes.add('')
    else:
        no.add('')

    hint = ' [Y/n] ' if default else ' [y/N] '

    while True:
        choice = input(prompt + hint).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print('Please respond with "yes" or "no"')


def configure():
    if not os.path.exists('.env'):
        if not yesno("the .env file does not exist, do you want to create it?", default=True):
            print('Aborting')
            exit(0)
        if not os.path.exists('.env.dist'):
            print('No .env.dist file found')
            exit(1)
        else:
            from shutil import copyfile
            copyfile('.env.dist', '.env')

    env = dotenv.load_dotenv('.env')
    if not env or not os.getenv('SECRET_KEY'):
        from django.core.management.utils import get_random_secret_key
        print('No SECRET_KEY found in .env file, generating one...')
        with open('.env', 'a') as f:
            f.write('\nSECRET_KEY=')
            f.write(get_random_secret_key())
            f.write('\n')

    # TODO rename ALLOWED_HOSTS to something more self-explanatory
    current_hosts = os.getenv('ALLOWED_HOSTS')
    print('Current ALLOWED_HOSTS: {}'.format(current_hosts))

    if yesno("Do you want to add ALLOWED_HOSTS?"):
        hosts = input("Enter a comma-separated list of allowed hosts: ")
        joined_hosts = current_hosts + ',' + hosts if current_hosts else hosts
        dotenv.set_key('.env', 'ALLOWED_HOSTS', joined_hosts)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    import django

    django.setup()

    if not os.path.exists('db.sqlite3'):
        if not yesno("No database found, do you want to create one?", default=True):
            print('Aborting')
            exit(0)

    from django.core.management import call_command
    call_command('migrate')

    if yesno("Do you want to create a superuser?"):
        from django.core.management import call_command
        call_command('createsuperuser')

    if not os.path.exists('static'):
        if yesno("No static directory found, do you want to create one?", default=True):
            os.mkdir('static')

    call_command('collectstatic', '--no-input')

    # if yesno("Do you want to load initial data?"):
    #   call_command('loaddata', 'initial_data.json')


if __name__ == '__main__':
    configure()
