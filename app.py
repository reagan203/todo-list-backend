from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from flask_mail import Mail
# resources.routes imports 
from resources.signup import Signup
from resources.login import Login
from resources.tasks import Task,Tasks


app= Flask(__name__)

CORS(app)

#CONFIGURING FLASK_MAIL
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT']=587 
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] ='41fb580871f53c76825c56eef08d2449'
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False

mail=Mail(app)

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
#routes 
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Task,'/task', '/task/<int:task_id>')
api.add_resource(Tasks,'/tasks')






if __name__ == '__main__':
    app.run(debug=True, port=5000)
