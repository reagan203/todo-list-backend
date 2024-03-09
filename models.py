from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash, generate_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

# UserModel represents users in the database
class UserModel(db.Model):
    """Model representing a user."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)  # Store password hash
    name = db.Column(db.String(120), nullable=False)
    
    # Method to get a user by ID
    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by ID."""
        return cls.query.get(user_id)

    # Method to set the password for the user
    def set_password(self, password):
        """Set the password for the user."""
        self.password = generate_password_hash(password)

    # Method to check if the provided password matches the stored password
    def check_password(self, password):
        """Check if the provided password matches the stored password."""
        return check_password_hash(self.password, password)

    # Method to convert the user object to a JSON-serializable dictionary
    def to_json(self):
        """Convert the user object to a JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# TaskModel represents tasks in the database
class TaskModel(db.Model):
    """Model representing a task."""
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    priority = db.Column(db.Enum("high", "medium", "low"), default="medium")
    status = db.Column(db.Enum("pending", "completed"), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Relationship with UserModel
    user = db.relationship('UserModel', backref=db.backref('tasks', lazy=True))

    # Method to convert the task object to a JSON-serializable dictionary
    def to_json(self):
        """Convert the task object to a JSON-serializable dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'user_id': self.user_id,
        }
