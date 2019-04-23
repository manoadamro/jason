from uuid import uuid4

from jason.database import db, model_factory, orm

Model = model_factory()
session_factory = orm.sessionmaker()


class Log(Model):
    __tablename__ = "logs"
    id = db.Column(
        db.String, primary_key=True, autoincrement=True, default=str(uuid4())
    )
    logger = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    module = db.Column(db.String, nullable=False)
    func = db.Column(db.String, nullable=False)
    lineno = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return (
            f"<User("
            f"id='{self.id}', "
            f"logger='{self.logger}', "
            f"created='{self.created.isoformat()}', "
            f"level='{self.level}', "
            f"service='{self.service}', "
            f"module='{self.module}', "
            f"func='{self.func}', "
            f"lineno={self.lineno}, "
            f"message='{self.message}'"
            f")>"
        )
