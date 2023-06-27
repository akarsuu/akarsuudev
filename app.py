from flask import Flask, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///likes.db'
db = SQLAlchemy(app)

#db model definition
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(45))
    likeCount = db.Column(db.Integer, default=0)
    totalLike = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/like', methods=['POST'])
def add_like():
    ip = request.remote_addr
    now = datetime.now()
    totalLike = totalLike

    # Check if IP is new 
    if Likes.query.filter_by(ip=ip).first():
        return jsonify({'message': "Like already counted",})
    # Create a new like record 

    like = Likes(ip=ip, date_created=now, likeCount=1)
    
    # add the like record to db

    db.session.add(like)
    db.session.commit()

    # update the totalLikes

    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
    max_id = Likes.query.with_entities(func.max(Likes.id)).scalar()
    Likes.query.filter_by(id=max_id).update({'totalLike': total_likes})
    db.session.commit()

    message = "Thank you for your support :)"

    return jsonify({'totalLike': total_likes, "message": message})

@app.route('/')
def index():
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
    return render_template('index.html', totalLike = total_likes)

if __name__ == '__main__':
    app.debug = True
    app.run()