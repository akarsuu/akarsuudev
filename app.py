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
    ip = request.headers.get('X-Forwarded-For')  # Get client's IP address from the header
    now = datetime.now()

    # Check if the IP has already liked the specific content
    existing_like = Likes.query.filter_by(ip=ip).first()

    if existing_like:
        # IP has already liked, so no action needed
        total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
        return jsonify({'message': "Like already counted", 'totalLike': total_likes or 0})

    # Calculate the totalLikes for the specific content
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar() or 0

    # Create a new like record for the specific content
    likes = Likes(ip=ip, date_created=now, likeCount=1, totalLike=total_likes + 1)

    # Add the like record to the database
    db.session.add(likes)
    db.session.commit()

    message = "Thank you for your support :)"
    return jsonify({'totalLike': total_likes + 1, "message": message})

@app.route('/')
def index():
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
    return render_template('index.html', totalLike = total_likes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)



   