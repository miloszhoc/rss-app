import json

from rss_app.database import models
from rss_app.database.models import db
from flask import render_template, jsonify, request, Blueprint
import requests
from sqlalchemy import exc
import rss_app.rss_parser
import rss_app.sendgrid_mail

bp = Blueprint('bp', __name__, template_folder='rss_app/templates')


# dodac walidacje na rss
@bp.route('/', methods=['GET', 'POST'])
def index():
    # prevents ajax error
    URL_LOCAL = request.url
    # if URL_LOCAL.startswith('http://'):
    #     URL_LOCAL = URL_LOCAL.replace('http://', 'https://', 1)

    error = ''
    debug_content = {'': ''}
    if request.method == "POST":
        if 'url_form' in request.form:
            url = request.form['url'].strip()
            # add new url to db
            add_url = requests.post('{}urls'.format(URL_LOCAL), data={'url': url})
            response = add_url.json()
            if not response['success']:
                error = response['error']

        elif 'email_form' in request.form:
            rss = requests.get('{}rss'.format(URL_LOCAL))
            response = rss.json()
            if not models.Url.query.all():
                error = 'Please add at least one RSS address'
            else:
                if response['success']:
                    try:
                        email = request.form['email']
                        html = rss_app.rss_parser.create_html(response['rss_content'])
                        debug_content = rss_app.sendgrid_mail.send_email(email, str(html))
                    except Exception as e:
                        print(e)
                        error = e
                if not response['success']:
                    error = response['error']

    # show all urls
    try:
        urls = requests.get('{}urls'.format(URL_LOCAL)).json()
    except json.decoder.JSONDecodeError:
        urls = {}
        error = 'No urls. Click button above to add your first RSS address!'

    return render_template('index.html', data={'urls': urls,
                                               'error': error,
                                               'url': URL_LOCAL,
                                               'debug_content': debug_content})


# get method
@bp.route('/urls', methods=['GET'])
def get_urls():
    schema = models.UrlSchema(many=True)
    urls = models.Url.query.order_by(models.Url.id.asc())
    data = schema.dump(urls)
    return jsonify(data)


@bp.route('/urls/<id>', methods=['GET'])
def get_url(id):
    schema = models.UrlSchema()
    url = models.Url.query.get(id)
    data = schema.dump(url)
    return jsonify(data)


# post method
@bp.route('/urls', methods=['POST'])
def add_url():
    success = False
    error = ''
    data = ''
    try:
        url = request.form['url']
        new_url = models.Url(url)
        db.session.add(new_url)
        db.session.commit()
        db.session.refresh(new_url)
        data = {'id': new_url.id, 'url': url}
        success = True
    except exc.IntegrityError:
        db.session.rollback()
        error = 'url already exists'
    except Exception as e:
        error = e.__repr__()
    finally:
        return {'success': success,
                'data': data,
                'error': error}


# delete method
@bp.route('/urls/<id>', methods=['DELETE'])
def delete_url(id):
    success = False
    error = None
    try:
        element = models.Url.query.filter_by(id=id).first()
        if element:  # if element exists
            models.Url.query.filter_by(id=id).delete()
            db.session.commit()
            success = True
        else:
            error = 'element does not exist'
    except Exception as e:
        error = 'element does not exist'
    finally:
        return {'success': success,
                'error': error}


# update method
@bp.route('/urls/<id>', methods=['PUT'])
def update_url(id):
    success = False
    error = None
    data = ''
    try:
        element = models.Url.query.get(id)
        url = element
        url_from_form = request.form['url'].strip()
        url.url = url_from_form
        db.session.commit()
        success = True
        data = {'new_url': url.url}
    except exc.IntegrityError:
        error = 'url already exists'
    except Exception as e:
        error = e.__repr__()
    finally:
        return {'success': success,
                'error': error,
                'data': data}


@bp.route('/rss', methods=['GET'])
def rss():
    error = ''
    rss_content = {}
    success = False
    try:
        schema = models.UrlSchema(many=True)
        urls = models.Url.query.order_by(models.Url.id.asc())
        data = schema.dump(urls)
        for content in rss_app.rss_parser.get_urls(data):
            rss_content[content] = rss_app.rss_parser.parse_rss(content)
        success = True
    except Exception as e:
        error = 'One of URLS is not RSS'

    return {'success': success,
            'rss_content': rss_content,
            'error': error}
