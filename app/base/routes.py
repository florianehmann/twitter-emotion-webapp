from app.base import bp
from app.base.forms import QueryForm
from app.inference import query_model, ModelQueryException
from flask import flash, render_template


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()

    render = None

    if form.validate_on_submit():
        try:
            tweet = form.tweet_text.data
            classifications = query_model(tweet)
            emotion = classifications[0]['label']
            confidence = f"{classifications[0]['score'] * 100:.1f}"

            render = render_template('base/index.html', form=form, tweet=tweet, emotion=emotion, confidence=confidence)
        except ModelQueryException as e:
            flash(f"Model Query Exception: {e}")

    if render is None:
        render = render_template('base/index.html', form=form)

    return render
