from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
# resources.routes imports 


app= Flask(__name__)

CORS(app)

#configure database
app.config['SQLALCHEMY_DATABASE_URI']=('sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY'] = ( 'super-secret')

#initialize database
db.init_app(app)

#initialise migrate for database migrations
migrate =Migrate(app ,db)

#initialise bcrypt for password hashing and jwt for authentication
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


api =Api(app)







if __name__ == '__main__':
    app.run(debug=True, port=5000)
