import requests
import flask as f
import flask_login as fl

app = f.Flask(__name__)


@app.route('/user/astrax/', defaults={'path': ''})
@app.route('/user/astrax/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@fl.login_required
def proxy(path):
    # Construct the URL to the proxied service
    url = f'http://localhost:33333/{path}'

    # Forward the request headers and data
    headers = {key: value for key, value in f.request.headers if key != 'Host'}
    data = f.request.get_data() if f.request.method in [
        'POST', 'PUT'] else None

    # Make the request to the proxied service
    resp = requests.request(
        method=f.request.method,
        url=url,
        headers=headers,
        data=data,
        cookies=f.request.cookies,
        allow_redirects=False
    )

    # Create a response to send back to the client
    excluded_headers = [
        'content-encoding', 'content-length', 'transfer-encoding', 'connection'
    ]
    headers = [(name, value) for name, value in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = f.Response(resp.content, resp.status_code, headers)
    return response
