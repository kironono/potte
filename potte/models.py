# coding: utf-8

import hashlib

from sqlalchemy import (
    engine_from_config,
    Table,
    Column,
    ForeignKey,
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


def initialize_sql(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    if not DBSession.registry.has():
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine


class User(Base):
    __tablename__ = 'user'

    username = Column(Unicode(256), primary_key=True)
    password = Column(Unicode(256), nullable=False)
    email = Column(Unicode(256), nullable=False)

    albums = relationship("Album", backref="user")
    photos = relationship("Photo", backref="user")

    @property
    def groups(self):
        return ["user"]

    @property
    def email_hash(self):
        md5 = hashlib.md5()
        md5.update(self.email.lower().encode('utf-8'))
        return md5.hexdigest()


class Album(Base):
    __tablename__ = 'album'

    id = Column(Unicode(255), primary_key=True)
    username = Column(Unicode(255), ForeignKey("user.username"))

    name = Column(Unicode(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    photos = relationship("Photo", secondary="album_has_photo",
                          backref="albums")


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Unicode(255), primary_key=True)
    username = Column(Unicode(255), ForeignKey("user.username"))

    filename = Column(Unicode(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    thumbnails = relationship("PhotoThumbnail", backref="photo")


class PhotoThumbnail(Base):
    __tablename__ = 'photo_thumbnail'

    id = Column(Unicode(255), primary_key=True)
    photo_id = Column(Unicode(255), ForeignKey('photo.id'))

    size = Column(Unicode(16))


album_has_photo = Table(
    'album_has_photo', Base.metadata,
    Column('album_id', Unicode(255), ForeignKey('album.id')),
    Column('photo_id', Unicode(255), ForeignKey('photo.id')),
)
