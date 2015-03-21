import json
import requests

from flask import Flask
from flask import request


HEADERS = {
    'Content-type': 'application/json'
}
URL = 'https://osf.io/api/v1/search/'

app = Flask(__name__)


@app.route('/contributor/')
def search_contributor():
    guid = request.args.get('guid')
    data = json.dumps({
        'query': {
            'query_string': {
                'default_field': '_all',
                'query': 'contributors_url{} AND (category:project OR category:component OR category:registration)'.format(guid),
                'analyze_wildcard': True,
                'lenient': True  # TODO, may not want to do this
            }
        }
    })

    results = requests.post(URL, headers=HEADERS, data=data).json()

    return json.dumps([{
        'title': x['title'],
        'contributors': x['contributors'],
        'contributors_url': x['contributors_url'],
        'url': x['url']
    } for x in results['results']], indent=4)


@app.route('/node/')
def search_node():
    guid = request.args.get('guid')
    data = json.dumps({
        'query': {
            'match': {
                'url': guid
            }
        }
    })

    results = requests.post(URL, headers=HEADERS, data=data).json()

    return json.dumps([{
        'contributors': x['contributors'],
        'contributors_url': x['contributors_url']
    } for x in results['results']], indent=4)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=1337,
        debug=True
    )
