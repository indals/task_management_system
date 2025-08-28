#!/usr/bin/env python3
"""
Management commands for the Task Management System
"""

import os
import sys
import click
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

@click.group()
def cli():
    """Task Management System CLI"""
    pass

@cli.command()
@click.option('--env', default='development', help='Environment to use')
def run(env):
    """Run the development server"""
    os.environ['FLASK_ENV'] = env
    from app import main
    main()

@cli.command()
@click.option('--env', default='development', help='Environment to use')
def init_db(env):
    """Initialize the database"""
    from dotenv import load_dotenv
    load_dotenv(f'env/.env.{env}')
    
    from app import create_app
    from config import get_config
    from app.utils.database import init_database
    
    app = create_app(get_config(env))
    with app.app_context():
        init_database()
        click.echo('✅ Database initialized successfully')

@cli.command()
@click.option('--message', '-m', required=True, help='Migration message')
@cli.option('--env', default='development', help='Environment to use')
def migrate(message, env):
    """Create a new migration"""
    from dotenv import load_dotenv
    load_dotenv(f'env/.env.{env}')
    
    import subprocess
    result = subprocess.run(['flask', 'db', 'migrate', '-m', message])
    sys.exit(result.returncode)

@cli.command()
@cli.option('--env', default='development', help='Environment to use')
def upgrade(env):
    """Apply database migrations"""
    from dotenv import load_dotenv
    load_dotenv(f'env/.env.{env}')
    
    import subprocess
    result = subprocess.run(['flask', 'db', 'upgrade'])
    sys.exit(result.returncode)

@cli.command()
def test():
    """Run the test suite"""
    import subprocess
    result = subprocess.run(['pytest', 'tests/', '-v'])
    sys.exit(result.returncode)

if __name__ == '__main__':
    cli()