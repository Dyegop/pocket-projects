"""
The test task is pretty simple: You need to create an API (only one endpoint like /data) with content negotiation which
answers with text/html and application/json (depending the header content-type) and this endpoint needs to have
pagination. So if you add a special query argument to the endpoint (up to you what are they), you can get the next
iteration of data and so on until the end of the "dataset".

Concerns:
    -The text/html version needs to be so simple using Jinja2 engine and a simple HTML table with the data
    (no need for styling or JavaScript at all).
    -For the backend the micro-framework to be used is Flask and you can use all the libraries as you want for this
    little test task.
    -The database needs to be ElasticSearch and it is up to you how to save the data, the used mapping for the
    documents, etc.
    -CSV sample data columns: id, inventory name, contact name, stock, last revenue, current revenue, refund,
    company name, categories, rating
    -Max items per scroll = 20. CSV has 5000 rows so you can do 250 scrolls.
    -Unittests could be included, are not mandatory but it would be great to see something about this.
    -The code needs to be uploaded to a git repository using gitflow if it is possible (use the SaaS that you prefer,
    Github, Gitlab, Bitbucket, etc) and share with me the URL when you finish.
"""

import database as db
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
es = db.ElasticSearchConnection()


@app.route('/')
def home():
    return render_template('home.jinja2')


@app.route('/data/<int:page>')
def data(page):
    """API route"""
    es_columns = db.FIELD_NAMES
    es_data = db.getData(page, es)
    if 'application/json' in request.headers['Accept']:
        return jsonify(es_data)
    else:
        results = [i['_source'] for i in es_data['hits']['hits']]
        if not results:
            return render_template('404.jinja2', message=f"Data not found for index {page} in ElasticSearch"
                                                         f"Try a different value")
        else:
            return render_template('table.jinja2', columns=es_columns, data=results)





# Run application
if __name__ == '__main__':
    app.run(port=5000, debug=True)
