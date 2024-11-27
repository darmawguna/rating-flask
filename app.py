"""Small apps to demonstrate endpoints with basic feature - CRUD"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
from api.rating.endpoints import review_endpoints
# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
Swagger(app)


# register the blueprint
app.register_blueprint(review_endpoints, url_prefix='/api/reviews')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
