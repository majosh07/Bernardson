from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Sequence, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class DailyStatus(Base):
    __tablename__ = 'daily_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='daily_status_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_reset: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


class Gifs(Base):
    __tablename__ = 'gifs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='gifs_pkey1'),
        UniqueConstraint('url', name='unique_gif_url')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('gifs_id_seq1'), primary_key=True)
    url: Mapped[str] = mapped_column(Text)
    tier: Mapped[str] = mapped_column(Text)

    daily_gifs: Mapped[List['DailyGifs']] = relationship('DailyGifs', back_populates='gif')
    user_favorites: Mapped[List['UserFavorites']] = relationship('UserFavorites', back_populates='gif')
    user_gifs: Mapped[List['UserGifs']] = relationship('UserGifs', back_populates='gif')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='users_pkey'),
        UniqueConstraint('user_id', name='users_username_key'),
        UniqueConstraint('username', name='users_username_key1')
    )

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    roll_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('10'))
    roll_streak: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    win_streak: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    can_add_gif: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    a_pity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    s_pity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    last_status: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    daily_gifs: Mapped[List['DailyGifs']] = relationship('DailyGifs', back_populates='user')
    user_favorites: Mapped[List['UserFavorites']] = relationship('UserFavorites', back_populates='user')
    user_gifs: Mapped[List['UserGifs']] = relationship('UserGifs', back_populates='user')


class DailyGifs(Base):
    __tablename__ = 'daily_gifs'
    __table_args__ = (
        ForeignKeyConstraint(['gif_id'], ['gifs.id'], ondelete='CASCADE', name='daily_gifs_gif_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='daily_gifs_author_id_fkey'),
        PrimaryKeyConstraint('id', name='daily_gifs_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gif_id: Mapped[int] = mapped_column(Integer)
    author: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    gif: Mapped['Gifs'] = relationship('Gifs', back_populates='daily_gifs')
    user: Mapped['Users'] = relationship('Users', back_populates='daily_gifs')


class UserFavorites(Base):
    __tablename__ = 'user_favorites'
    __table_args__ = (
        ForeignKeyConstraint(['gif_id'], ['gifs.id'], ondelete='CASCADE', name='fk_gif'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='fk_user'),
        PrimaryKeyConstraint('id', name='user_favorites_pkey'),
        UniqueConstraint('user_id', 'gif_id', name='unique_user_gif_fav')
    )

    user_id: Mapped[int] = mapped_column(BigInteger)
    gif_id: Mapped[int] = mapped_column(Integer)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    favorited_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    gif: Mapped['Gifs'] = relationship('Gifs', back_populates='user_favorites')
    user: Mapped['Users'] = relationship('Users', back_populates='user_favorites')


class UserGifs(Base):
    __tablename__ = 'user_gifs'
    __table_args__ = (
        ForeignKeyConstraint(['gif_id'], ['gifs.id'], ondelete='CASCADE', name='fk_gif'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='fk_user'),
        PrimaryKeyConstraint('id', name='gifs_pkey'),
        UniqueConstraint('user_id', 'gif_id', name='user_gif_unique')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('gifs_id_seq'), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    gif_id: Mapped[int] = mapped_column(Integer)
    obtain_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    gif: Mapped['Gifs'] = relationship('Gifs', back_populates='user_gifs')
    user: Mapped['Users'] = relationship('Users', back_populates='user_gifs')
