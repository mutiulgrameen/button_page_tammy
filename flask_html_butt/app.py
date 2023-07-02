from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)
#print("Hello Nerd 1")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

@app.route('/')
def home():
    messages = Message.query.all()
    #print("Hello Nerd 2")
    return render_template('button_page_1.html', messages=messages)

@socketio.on('connect')
def handle_connect():
    emit('user_connected', {'message': 'A user has connected'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    emit('user_disconnected', {'message': 'A user has disconnected'}, broadcast=True)


# def handle_button_click(data):
#     emit('button_clicked', {'message': data['message']}, broadcast=True)
@socketio.on('message')
def handle_button_click(data):
    message_content = data['message']
    message = Message(content=message_content)
    db.session.add(message)
    db.session.commit()
    print(message)
    emit('button_clicked', {'message': message_content}, broadcast=True)

if __name__ == '__main__':
    #print("Hello Nerd 2")
    with app.app_context():
    #    print("Hello Nerd 3")
        db.create_all()
    #    print("Hello Nerd 4")
    socketio.run(app)
    #print("Hello Nerd 5")
