from _init_ import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    userId = db.Column(db.Integer,db.foreignKey('user.id'),nullable = False)
    iscompleted = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return f'Todo ({self.name})'
    