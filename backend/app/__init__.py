from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from app.routes import auth, doctors, patients, appointments
    app.register_blueprint(auth.bp)
    app.register_blueprint(doctors.bp)
    app.register_blueprint(patients.bp)
    app.register_blueprint(appointments.bp)
    
    return app
