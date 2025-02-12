from flask import Flask, render_template, request , jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secretkey'
db = SQLAlchemy(app)


class Love(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="Not Clicked")
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name
        
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def valentines_card():
    name = None 
    user_status = "Not Clicked"
    if request.method == 'POST':
        name = request.form.get('name') 
        if name:
            new_love = Love(name)
            db.session.add(new_love)
            db.session.commit()
            session['userId'] = new_love.id
            user_status = new_love.status
    return render_template('index.html', name=name)


@app.route('/clicked_yes', methods=['GET', 'POST'])
def clicked_yes():
    if 'userId' in session:
        love_entry = Love.query.get(session['userId'])
        if love_entry:
            love_entry.status = "Clicked Yes"
            db.session.commit()
            return jsonify({'success': True, 'status': 'Clicked'})
    return jsonify({'success': False, 'message': 'User not found'})


if __name__ == '__main__':
    app.run(debug=True)
