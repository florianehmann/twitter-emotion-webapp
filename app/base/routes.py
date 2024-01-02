"""Endpoints of the base Module"""

from flask import current_app, flash, render_template, request

from app import db
from app.base import bp
from app.base.forms import QueryForm
from app.inference import query_model, ModelLoadingException, ModelQueryException
from app.models import EMOTION_INDEX, UserRequest


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Main page with form to request classifications"""

    form = QueryForm()
    common_kwargs = {'form': form}

    render = None
    if form.validate_on_submit():
        render = process_user_request(form, common_kwargs)

    if render is None:
        render = render_template('base/index.html', **common_kwargs)

    return render


@bp.route('/privacy')
def privacy():
    """Privacy statement of the site"""
    return render_template('base/privacy.html')


def process_user_request(form, common_kwargs):
    """Query the model, log the request and generate the response HTML"""

    render = None
    tweet_text = form.tweet_text.data
    user_classification = form.user_classification.data
    user_ip = request.headers.get('X-Forwarded-For') or 'unavailable'

    try:
        classifications = query_model(tweet_text)
        log_user_request(tweet_text, user_ip)
        store_request_in_database(tweet_text, user_ip, user_classification)
        render = render_result(tweet_text, classifications, common_kwargs)

    except ModelQueryException as e:
        current_app.logger.error(f"Language Model Error: {e}")
        flash(f"There was an error with the language model: {e}")

    except ModelLoadingException:
        current_app.logger.warning("Language model currently loading")
        flash("Model is currently loading, try again in 20 seconds.")

    return render


def store_request_in_database(tweet_text, user_ip, user_classification: str):
    # pylint: disable=missing-function-docstring
    class_index = EMOTION_INDEX[user_classification] if user_classification in EMOTION_INDEX else None
    user_request = UserRequest(tweet_text=tweet_text, user_ip=user_ip, user_classification=class_index)
    db.session.add(user_request)
    db.session.commit()


def render_result(tweet_text, classifications, common_kwargs):
    """Renders the results of a classification request into HTML"""

    emotion = classifications[0]['label']
    confidence = f"{classifications[0]['score'] * 100:.1f}"
    render = render_template('base/index.html', tweet=tweet_text, emotion=emotion,
                             confidence=confidence, **common_kwargs)
    return render


def log_user_request(tweet_text, user_ip):
    # pylint: disable=missing-function-docstring
    current_app.query_logger.info(f"{user_ip} - \"{tweet_text}\"")
    current_app.logger.debug(f"Querying model on \"{tweet_text}\"")
