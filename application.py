from flask import render_template
import requests
from config import app, db, jsonify, request
import models
from sqlalchemy import exc
import rss_parser
import sendgrid_mail


# dodac walidacje na rss
@app.route('/', methods=['GET', 'POST'])
def index():
    URL_LOCAL = request.url
    error = ''
    frame_content = ''

    # show all urls
    urls = requests.get('{}/urls'.format(URL_LOCAL)).json()

    if request.method == "POST":
        if 'url_form' in request.form:
            url = request.form['url']
            # add new url to db
            add_url = requests.post('{}/urls'.format(URL_LOCAL), data={'url': url})
            response = add_url.json()
            if not response['success']:
                error = response['error']

        elif 'email_form' in request.form:
            email = request.form['email']
            requests.post('{}/mail'.format(URL_LOCAL), data={'email': email})

    return render_template('index.html', data={'urls': urls,
                                               'error': error,
                                               'url': URL_LOCAL,
                                               'frame_content': frame_content})


# get method
@app.route('/urls', methods=['GET'])
def get_urls():
    schema = models.UrlSchema(many=True)
    urls = models.Url.query.order_by(models.Url.id.asc())
    data = schema.dump(urls)
    return jsonify(data)


@app.route('/urls/<id>', methods=['GET'])
def get_url(id):
    schema = models.UrlSchema()
    url = models.Url.query.get(id)
    data = schema.dump(url)
    return jsonify(data)


# post method
@app.route('/urls', methods=['POST'])
def add_url():
    success = False
    error = ''
    data = ''
    try:
        url = request.form['url']
        new_url = models.Url(url)
        db.session.add(new_url)
        db.session.commit()
        data = url
        success = True
    except exc.IntegrityError:
        error = 'url already exists'
    except Exception:
        error = 'unknown'
    finally:
        return {'success': success,
                'data': data,
                'error': error}


# delete method
@app.route('/urls/<id>', methods=['DELETE'])
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
        error = 'unknown'
    finally:
        return {'success': success,
                'error': error}


# update method
@app.route('/urls/<id>', methods=['PUT'])
def update_url(id):
    success = False
    error = None
    try:
        element = models.Url.query.get(id)
        url = element
        url_from_form = request.form['url']
        url.url = url_from_form
        db.session.commit()
        success = True
    except exc.IntegrityError:
        error = 'url already exists'
    except Exception:
        error = 'unknown'
    finally:
        return {'success': success,
                'error': error}


@app.route('/mail', methods=['POST'])
def mail():
    d = {}
    email = request.form['email']
    schema = models.UrlSchema(many=True)
    urls = models.Url.query.order_by(models.Url.id.asc())
    data = schema.dump(urls)
    for content in rss_parser.get_urls(data):
        d[content] = rss_parser.parse_rss(content)
    html = rss_parser.create_html(d)
    sendgrid_mail.send_email(email, str(html))
    return d


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
