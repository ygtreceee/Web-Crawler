from flask import Flask, send_file

app = Flask(__name__)

@app.route('/log')
def get_log():
    filepath = './log.xml'
    return send_file(filepath, mimetype='text/plain;charset=UTF-8')

if __name__ == '__main__':
    app.run()