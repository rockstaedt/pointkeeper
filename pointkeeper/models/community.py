from pointkeeper.extensions import db


class Community(db.Model):
    __tablename__ = "communities"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pin = db.Column(db.String(50), nullable=False)
    downside = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Table(ID: {self.id}, Name: {self.name})"
