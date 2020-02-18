from flask import Flask, request, jsonify
from flask_cors import CORS
import time
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
    return '테스트입니다.'
 
@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()
    return jsonify(user)

@app.route('/environments/<language>')
def environments(language):
    i = 0
    while i < 10000:
        i += 1
        time.sleep(0.001) 
    return jsonify({"language":language})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=8001)
