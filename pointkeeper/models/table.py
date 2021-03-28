from pointkeeper.extensions import db


class Table(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pin = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Table(ID: {self.id}, Name: {self.name})"
