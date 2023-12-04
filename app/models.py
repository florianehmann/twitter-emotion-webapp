"""Database Models/Schema of the Application"""

from datetime import datetime, timezone
from textwrap import shorten
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


# pylint: disable=too-few-public-methods
class Tweet(db.Model):
    """Text Content of a Tweet"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    text: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True)

    user_queries: so.WriteOnlyMapped['UserQuery'] = so.relationship('UserQuery', back_populates='tweet')
    model_response: so.Mapped['ModelResponse'] = so.relationship('ModelResponse', back_populates='tweet')

    def __repr__(self):
        wrapped_content = shorten(self.text, 40)
        return f"<Tweet {self.id}: \"{wrapped_content}\">"


# pylint: disable=too-few-public-methods
class UserQuery(db.Model):
    """User Query to the App"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tweet_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Tweet.id), index=True)
    user_classification: so.Mapped[Optional[str]] = so.mapped_column(sa.Integer)
    user_ip: so.Mapped[str] = so.mapped_column(sa.String(16))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    tweet: so.Mapped[Tweet] = so.relationship('Tweet', back_populates='user_queries')

    def __repr__(self):
        wrapped_content = shorten(self.tweet.text, 40)
        return f"<UserQuery {self.id}: \"{wrapped_content}\">"


# pylint: disable=too-few-public-methods
class ModelResponse(db.Model):
    """Response of the Model to a Given Tweet Input"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tweet_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Tweet.id))
    content: so.Mapped[dict] = so.mapped_column(sa.JSON())
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    tweet: so.Mapped[Tweet] = so.relationship('Tweet', back_populates='model_response')

    def __repr__(self):
        wrapped_content = shorten(self.tweet.text, 40)
        return f"<ModelResponse {self.id}: \"{wrapped_content}\">"
