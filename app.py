from flask import Flask, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
from flask_cors import CORS

app = Flask (__name__,
            static_url_path='',
            static_folder='../static')
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
    
    # Check if the IP has already liked the specific content
    existing_like = Likes.query.filter_by(ip=ip).first()
    if existing_like:
        return jsonify({'message': "Like already counted", 'totalLike':total_likes})
  

    # Create a new like record for the specific content
    like = Likes(ip=ip, date_created=now, likeCount=1)
    
    # Add the like record to the database
    db.session.add(like)
    db.session.commit()

    # Update the totalLikes for the specific content
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()

    message = "Thank you for your support :)"

    return jsonify({'totalLike': total_likes, "message": message})

@app.route('/')
def index():
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
    return render_template('index.html', totalLike = total_likes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
