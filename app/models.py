"""Database Models/Schema of the Application"""

from datetime import datetime, timezone
from textwrap import shorten

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


# pylint: disable=too-few-public-methods
class UserRequest(db.Model):
    """User Query to the App"""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tweet_text: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_ip: so.Mapped[str] = so.mapped_column(sa.String(16))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        wrapped_content = shorten(self.tweet_text, 40)
        return f"<UserRequest {self.id}: \"{wrapped_content}\">"
