from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256

# Creating database extension instance
db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    albums = db.relationship(
        "Album", back_populates="artists", cascade="all, delete-orphan"
    )


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    mbid = db.Column(db.Text, nullable=False, unique=True)
    release_date = db.Column(db.Date, nullable=False)
    genres = db.Column(db.Text)

    # Linking album to artist and cover
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artist", back_populates="albums")


class Cover(db.Model):
    __tablename__ = "covers"

    id = db.Column(db.Integer, primary_key=True)
    cover_art_url = db.Column(db.Text)

    album_id = db.Column(
        db.Integer, db.ForeignKey("albums.id"), unique=True, nullable=False
    )
    album = db.relationship("Album", back_populates="cover")
