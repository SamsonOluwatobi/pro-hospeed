from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from app.email import mail
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import and register blueprints
        from app.main.routes import main
        from app.auth.routes import auth
        from app.doctor.routes import doctor
        from app.patient.routes import patient
        
        app.register_blueprint(main)
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(doctor, url_prefix='/doctor')
        app.register_blueprint(patient, url_prefix='/patient')

        # Error handlers
        @app.errorhandler(404)
        def not_found_error(error):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return render_template('500.html'), 500

        # Create database tables
        db.create_all()

    @app.context_processor
    def utility_processor():
        return {
            'now': datetime.utcnow()
        }

    return app

from app import models
