"""Forms of the base Module"""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


MAX_TWEET_LEN = 280
TWEET_TOO_LONG_MSG = f"Your tweet is too long. Can at most be {MAX_TWEET_LEN} characters. Yours is %(max)d."


class QueryForm(FlaskForm):
    """Form to Query the Language Model for a Classification"""

    tweet_text = TextAreaField(validators=[DataRequired(), Length(max=280, message=TWEET_TOO_LONG_MSG)],
                               render_kw={'maxlength': MAX_TWEET_LEN, 'rows': 3, 'cols': 100})
    user_classification = SelectField(choices=[
        ('None', ''),
        ('sadness', 'Sadness'),
        ('joy', 'Joy'),
        ('love', 'Love'),
        ('anger', 'Anger'),
        ('fear', 'Fear'),
        ('surprise', 'Surprise'),
    ], label='What would you say? (optional)')
    submit_button = SubmitField('Analyze!')
