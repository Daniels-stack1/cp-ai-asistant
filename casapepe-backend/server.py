from flask import Flask
from flask_cors import CORS
from api.routes import api_blueprint
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
