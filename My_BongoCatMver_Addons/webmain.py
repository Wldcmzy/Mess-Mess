from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/l4d2mymotd', methods= ['GET'])
def l4d2mymotd():
    return render_template('mymotd.html')

@app.route('/l4d2myhost', methods= ['GET'])
def l4d2myhost():
    return render_template('myhost.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 37201)