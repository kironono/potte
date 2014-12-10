# coding: utf-8

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    username = Column(Unicode(256), primary_key=True)
    password = Column(Unicode(256), nullable=False)
    email = Column(Unicode(256), nullable=False)

    albums = relationship("Album", backref="user")
    photos = relationship("Photo", backref="user")


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(256), ForeignKey("user.username"))

    name = Column(Unicode(256), nullable=False)
    created_at = Column(DateTime, nullable=False)

    photos = relationship("Photo", secondary="album_has_photo",
                          backref="albums")


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Unicode(256), primary_key=True)
    username = Column(Unicode(256), ForeignKey("user.username"))

    created_at = Column(DateTime, nullable=False)

    thumbnails = relationship("PhotoThumbnail", backref="photo")


class PhotoThumbnail(Base):
    __tablename__ = 'photo_thumbnail'

    id = Column(Unicode(256), primary_key=True)
    photo_id = Column(Unicode(256), ForeignKey('photo.id'))

    size = Column(Unicode(16))


album_has_photo = Table(
    'album_has_photo', Base.metadata,
    Column('album_id', Integer, ForeignKey('album.id')),
    Column('photo_id', Unicode(256), ForeignKey('photo.id')),
)
