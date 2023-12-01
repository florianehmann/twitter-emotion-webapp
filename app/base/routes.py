"""Endpoints of the base Module"""

from flask import current_app, flash, render_template

from app.base import bp
from app.base.forms import QueryForm
from app.inference import query_model, ModelLoadingException, ModelQueryException


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Main Page with Form to Query the Classification Model"""

    form = QueryForm()

    render = None
    if form.validate_on_submit():
        try:
            tweet = form.tweet_text.data.strip()
            current_app.query_logger.info(f"\"{tweet}\"")
            current_app.logger.debug(f"Querying model on \"{tweet}\"")
            classifications = query_model(tweet)
            emotion = classifications[0]['label']
            confidence = f"{classifications[0]['score'] * 100:.1f}"

            render = render_template('base/index.html', form=form, tweet=tweet, emotion=emotion, confidence=confidence)
        except ModelQueryException as e:
            current_app.logger.error(f"Language Model Error: {e}")
            flash(f"There was an error with the language model: {e}")
        except ModelLoadingException:
            current_app.logger.warning("Language model currently loading")
            flash("Model is currently loading, try again in 20 seconds.")

    if render is None:
        render = render_template('base/index.html', form=form)

    return render
