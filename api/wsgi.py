import os
from http import HTTPStatus

def wsgi_handler(app, event, context):
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    query_string = '&'.join([f"{k}={v}" for k, v in event.get('queryStringParameters', {}).items()])
    body = event.get('body', '')

    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)) if body else '0',
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': body.encode() if body else b'',
        'wsgi.errors': os.sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    response = {'statusCode': HTTPStatus.OK, 'headers': {}, 'body': ''}

    def start_response(status, response_headers, exc_info=None):
        status_code = int(status.split()[0])
        response['statusCode'] = status_code
        response['headers'].update(dict(response_headers))

    response_body = app(environ, start_response)
    response['body'] = b''.join(response_body).decode('utf-8')

    return response
