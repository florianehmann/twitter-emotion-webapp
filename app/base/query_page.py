"""Functionality of the query page"""

from math import ceil

from flask import request, current_app, flash, render_template
from markupsafe import Markup
import plotly
import plotly.express as px

from app import db
from app.inference import query_model, ModelQueryException, ModelLoadingException
from app.models import EMOTION_INDEX, UserRequest

PLOT_COLOR = {
    'joy': 'orange',
    'anger': 'red',
    'sadness': 'blue',
    'love': 'pink',
    'surprise': 'green',
    'fear': 'purple',
}


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

    except ModelLoadingException as e:
        rounded_time_estimate = ceil(e.time_estimate / 5) * 5
        common_kwargs['submit_timeout'] = rounded_time_estimate
        current_app.logger.warning(f"Language model currently loading. Approx {e.time_estimate:.1f}s remaining")
        flash(f"The AI model is currently booting up. Results loading in {rounded_time_estimate} seconds...")

    return render


def store_request_in_database(tweet_text, user_ip, user_classification: str):
    # pylint: disable=missing-function-docstring
    class_index = EMOTION_INDEX[user_classification] if user_classification in EMOTION_INDEX else None
    user_request = UserRequest(tweet_text=tweet_text, user_ip=user_ip, user_classification=class_index)
    db.session.add(user_request)
    db.session.commit()


def log_user_request(tweet_text, user_ip):
    # pylint: disable=missing-function-docstring
    current_app.query_logger.info(f"{user_ip} - \"{tweet_text}\"")
    current_app.logger.debug(f"Querying model on \"{tweet_text}\"")


def render_result(tweet_text, classifications, common_kwargs):
    """Renders the results of a classification request into HTML"""

    emotion = classifications[0]['label']
    confidence = f"{classifications[0]['score'] * 100:.1f}"
    radar_plot = generate_plot(classifications)
    render = render_template('base/index.html', tweet=tweet_text, emotion=emotion, plot=radar_plot,
                             confidence=confidence, **common_kwargs)
    return render


def generate_plot(classifications):
    """Generate a radar plot based on the scores for each label"""
    color = PLOT_COLOR[classifications[0]['label']]
    data = {
        'score': [row['score'] for row in classifications],
        'label': [row['label'] for row in classifications],
    }

    fig = px.line_polar(data, r='score', theta='label', line_close=False, hover_data='label',
                        color_discrete_sequence=[color], line_shape='spline')
    fig.update_traces(fill='toself')

    return Markup(plotly.io.to_html(fig, full_html=False, div_id='plot', include_plotlyjs='cdn'))
