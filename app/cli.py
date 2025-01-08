import click
from flask.cli import with_appcontext
from app import db
from app.models import User

@click.command('create-admin')
@click.option('--force', is_flag=True, help='Overwrite existing admin user')
@with_appcontext
def create_admin(force):
    """Create an admin user."""
    admin_email = click.prompt('Admin email', type=str)
    admin_password = click.prompt('Admin password', type=str, hide_input=True)
    
    # Check if admin already exists
    admin = User.query.filter_by(email=admin_email).first()
    if admin:
        if not force and not click.confirm('Admin user already exists. Do you want to overwrite?'):
            click.echo('Operation cancelled.')
            return
        # Update existing admin
        admin.username = 'admin'
        admin.user_type = 'admin'
        admin.is_verified = True
        admin.set_password(admin_password)
    else:
        # Create new admin user
        admin = User(
            username='admin',
            email=admin_email,
            user_type='admin',
            is_verified=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
    
    db.session.commit()
    click.echo('Admin user created/updated successfully!') 