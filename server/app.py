#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# endpoint to clear session


@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200


@app.route('/articles')
def index_articles():
    articles_lc = [article.to_dict() for article in Article.query.all()]

    response = make_response(jsonify(articles_lc), 200)

    response.headers["Content-Type"] = "application/json"
    return response


# endpoint for viewing articles


@app.route('/articles/<int:id>')
def show_article(id):
    # set page_views to 0 if first request, else increment by 1
    session["page_views"] = session.get("page_views", 0) + 1

    article = Article.query.filter_by(id=id).first()

    article_dict = article.to_dict()

    # article_dict = {"author": article.author,
    #                 "title": article.title,
    #                 "content": article.content,
    #                 "preview": article.preview,
    #                 "minutes_to_read": article.minutes_to_read}

    # check if the user has viewed 3 or fewer pages
    if session["page_views"] <= 3:
        response = make_response(jsonify(
            article_dict
        ), 400)

        response.headers["Content-Type"] = "application/json"
        return response

    else:
        response_body = {
            'message': 'Maximum pageview limit reached'
        }

        response = make_response(jsonify(
            response_body, 401
        ))

        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
