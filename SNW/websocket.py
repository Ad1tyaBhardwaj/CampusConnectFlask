from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit
import os
import sys
import json


from flask import Flask, render_template
import sys
import json

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('connect')
def we_connect():
    try:
        #Read
        f = open("liveuser.txt","r")
        data = f.read()
        tem = {"counter": int(json.loads(data).get("counter")) + 1}
        f.close()
        emit('user', tem, broadcast = True)
    except :
        fw = open('test.txt','w', encoding = 'utf-8')
        fw.write(json.dumps({"counter": 0}))
        fw.close()
        emit('user',{"counter":0},broadcast = True)


@socketio.on('disconnect')
def we_disconnect():
    #Read
    f = open("liveuser.txt","r")
    data = f.read()
    tem = {"counter": int(json.loads(data).get("counter")) - 1}
    f.close()

    #write
    fw = open('test.txt','w', encoding = 'utf-8')
    fw.write(json.dumps({tem}))
    fw.close()
    emit('user',tem,broadcast = True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('livecount.html')

if __name__ == '__main__':
    app.run(debug=True)




if __name__ == '__main__':
    socketio.run(app)
