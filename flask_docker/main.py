import random
import string
from flask import Flask, request
import time

app = Flask(__name__)

start_url = "<br><br><a href='/'>main page</a>"

@app.route("/")
def hello_world():
    return '''
        <h2>main page</h2>
        <ul>
            <li><a href="/whoami">whoami</a></li>
            <li><a href="/source_code">source_code</a></li>
            <li><a href="/random?length=42&specials=1&digits=0">random</a></li>
        </ul>
    '''

@app.route("/whoami/")
def whoami():
    user_agent = request.headers.get('User-Agent')
    client_ip = request.environ.get('REMOTE_ADDR')
    srv_time = time.strftime('%H:%M:%S')

    return f'''
        <h2>whoami</h2>
        <p>User agent: {user_agent}</p>
        <p>IP: {client_ip}</p>
        <p>Server Time: {srv_time}</p>
    ''' + start_url

@app.route("/source_code/")
def source_code():
    return f"<h2>source_code</h2><p>{open(__file__).read()}</p>" + start_url

def check(x, a, b):
    return x is None or x.isdigit() and a <= int(x) <= b

@app.route("/random/")
def gen_random(length = 0, specials = 0, digits = 0):
    spec = '!"№;%:?*()_+'
    symbols = string.ascii_letters

    args = request.args
    length = args.get('length')
    specials = args.get('specials')
    digits = args.get('digits')

    if check(length, 1, 100) and check(specials, 0, 1) and check(digits, 0, 1):
        length = 0 if length is None else int(length)
        specials = 0 if specials is None else int(specials)
        digits = 0 if digits is None else int(digits)

        if specials:
            symbols += spec
        if digits:
            symbols += string.digits

        rnd_string = ''.join(symbols[random.randrange(0, len(symbols))] for _ in range(length))

        res = f'''
            <h2>random</h2>
            <p>Current params: [{length=}, {specials=}, {digits=}]</p>
            <p>Random string: {rnd_string}</p>
        '''
    else:
        res = f'''
            <h2>random</h2>
            <p>Wrong params!!!</p>
            <p>Params must be: [length in [1..100], specials in {{0, 1}}, digits in {{0, 1}}]</p>
            <p>Current params: [{length=}, {specials=}, {digits=}]</p>            
        '''
    return res + start_url

# in terminal
# flask --app main run
# flask --app main --debug run

if __name__ == '__main__':
    app.run(debug=True)
