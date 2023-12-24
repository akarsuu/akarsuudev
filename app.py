from flask import Flask, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
from flask_cors import CORS
import threading
import time


app = Flask (__name__,
            static_url_path='',
            static_folder='../static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///likes.db'


app.config['SQLALCHEMY_BINDS'] = {
    'countingDB': 'sqlite:///countingDB.db',
    'countingReaction' : 'sqlite:///countingReaction.db'
}

db = SQLAlchemy(app)

#db model definition
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(45))
    likeCount = db.Column(db.Integer, default=0)
    totalLike = db.Column(db.Integer, default=0)

class Countdown(db.Model):
    __bind_key__ = 'countingDB'
    id = db.Column(db.Integer, primary_key=True)
    countdown_seconds_a = db.Column(db.Integer, default=timedelta(days=200).total_seconds)
    total_a = db.Column(db.Integer, default=20)
    countdown_seconds_b = db.Column(db.Integer, default=timedelta(seconds=788).total_seconds)
    total_b = db.Column(db.Integer, default=401468)
    countdown_seconds_c = db.Column(db.Integer, default=timedelta(seconds=5).total_seconds)
    total_c = db.Column(db.Integer, default=129000000)
    countdown_second_d = db.Column(db.Integer, default=timedelta(days=97).total_seconds)
    total_d = db.Column(db.Integer, default=311)
    countdown_second_e = db.Column(db.Integer, default=timedelta(seconds=555).total_seconds)
    total_e = db.Column(db.Integer, default=427545)
    countdown_second_f = db.Column(db.Integer, default=lambda: int(timedelta(seconds=86100).total_seconds()))
    total_f = db.Column(db.Integer, default=3757)
    countdown_second_g = db.Column(db.Integer, default=timedelta(seconds=807).total_seconds)
    total_g = db.Column(db.Integer, default=886601)
    countdown_second_h = db.Column(db.Integer, default=timedelta(seconds=15).total_seconds)
    total_h = db.Column(db.Integer, default=169600000)
    countdown_second_i = db.Column(db.Integer, default=timedelta(seconds=1740).total_seconds)
    total_i = db.Column(db.Integer, default=77542254)
    countdown_second_j = db.Column(db.Integer, default=timedelta(seconds=15).total_seconds)
    total_j = db.Column(db.Integer, default=126000000)
    countdown_second_k = db.Column(db.Integer, default=timedelta(seconds=1).total_seconds)  
    total_k = db.Column(db.Integer, default=14617500000)
    countdown_second_l = db.Column(db.Integer, default=timedelta(seconds=1).total_seconds)  
    total_l = db.Column(db.Integer, default=1103800000000)
    total_m = db.Column(db.Integer, default=24484)
    countdown_second_m = db.Column(db.Integer, default=timedelta(seconds=28800).total_seconds)

class CountdownReaction(db.Model):
    __bind_key__ = 'countingReaction'
    id = db.Column(db.Integer, primary_key=True)
    ip_countdown_reaction = db.Column(db.String(45))
    like_countdown = db.Column(db.Integer, default=0)
    dislike_countdown = db.Column(db.Integer, default=0)
    angry_countdown = db.Column(db.Integer, default=0)
    sad_countdown = db.Column(db.Integer, default=0)
    surprised_countdown = db.Column(db.Integer, default=0)
    denial_countdown = db.Column(db.Integer, default=0)
    total_like = db.Column(db.Integer, default=0)
    total_dislike = db.Column(db.Integer, default=0)
    total_angry = db.Column(db.Integer, default=0)
    total_sad = db.Column(db.Integer, default=0)
    total_surprised = db.Column(db.Integer, default=0)
    total_denial = db.Column(db.Integer, default=0)
    




with app.app_context():
    db.create_all()


def countdown_generic(countdown_attr, total_attr, initial_seconds, default_total):
    with app.app_context():
        while True:
            start_time = datetime.now()
            countdown = Countdown.query.first()
            if countdown is None:
                with app.app_context():
                    initial_countdown = Countdown(**{countdown_attr: initial_seconds, total_attr: default_total})
                    db.session.add(initial_countdown)
                    db.session.commit()
                countdown = Countdown.query.first()
            
            countdown_seconds = getattr(countdown, countdown_attr)
        
            if countdown_seconds > 0:
                setattr(countdown, countdown_attr, countdown_seconds -1)
            else:
                setattr(countdown, countdown_attr, initial_seconds)
                setattr(countdown, total_attr, getattr(countdown, total_attr) + (19 if countdown_attr == 'countdown_second_k' else (640 if countdown_attr == 'countdown_second_l' else 1)))
                '''
                setattr(countdown, total_attr, getattr(countdown, total_attr)  + (19 if countdown_attr == 'countdown_second_k' else 1))
                setattr(countdown, total_attr, getattr(countdown, total_attr) + (640 if countdown_attr == 'countdown_second_l' else 1))
               '''
            db.session.commit()
            remaining_time = str(timedelta(seconds=getattr(countdown, countdown_attr)))
            total_loops = getattr(countdown, total_attr)
            elapsed_time = (datetime.now() - start_time).total_seconds()
            sleep_time = max(1 - elapsed_time, 0)
            time.sleep(sleep_time)


countdown_thread_a = threading.Thread(target=countdown_generic, args=('countdown_seconds_a', 'total_a', timedelta(days=97).total_seconds(), 20))
countdown_thread_b = threading.Thread(target=countdown_generic, args=('countdown_seconds_b', 'total_b', timedelta(seconds=788).total_seconds(), 401468))
countdown_thread_c = threading.Thread(target=countdown_generic, args=('countdown_seconds_c', 'total_c', timedelta(seconds=5).total_seconds(), 129000000))
countdown_thread_d = threading.Thread(target=countdown_generic, args=('countdown_second_d', 'total_d', timedelta(seconds=15).total_seconds(), 311))
countdown_thread_e = threading.Thread(target=countdown_generic, args=('countdown_second_e', 'total_e', timedelta(seconds=555).total_seconds(), 427545))
countdown_thread_f = threading.Thread(target=countdown_generic, args=('countdown_second_f', 'total_f', timedelta(seconds=86100).total_seconds(), 3757))
countdown_thread_g = threading.Thread(target=countdown_generic, args=('countdown_second_g', 'total_g', timedelta(seconds=807).total_seconds(), 886601))
countdown_thread_h = threading.Thread(target=countdown_generic, args=('countdown_second_h', 'total_h', timedelta(seconds=15).total_seconds(), 169600000))
countdown_thread_i = threading.Thread(target=countdown_generic, args=('countdown_second_i', 'total_i', timedelta(seconds=1740).total_seconds(), 77542254))
countdown_thread_j = threading.Thread(target=countdown_generic, args=('countdown_second_j', 'total_j', timedelta(seconds=15).total_seconds(),126000000))
countdown_thread_k = threading.Thread(target=countdown_generic, args=('countdown_second_k', 'total_k', timedelta(seconds=1).total_seconds(), 19))
countdown_thread_l = threading.Thread(target=countdown_generic, args=('countdown_second_l', 'total_l', timedelta(seconds=1).total_seconds(), 640))
countdown_thread_m = threading.Thread(target=countdown_generic, args=('countdown_second_m', 'total_m', timedelta(seconds=28800).total_seconds(), 24484))



countdown_thread_a.start()
countdown_thread_b.start()
countdown_thread_c.start()
countdown_thread_d.start()
countdown_thread_e.start()
countdown_thread_f.start()
countdown_thread_g.start()
countdown_thread_h.start()
countdown_thread_i.start()
countdown_thread_j.start()
countdown_thread_k.start()
countdown_thread_l.start()
countdown_thread_m.start()


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



@app.route('/countdownVotes', methods=['POST'])
def countdown_votes():
    # get ip 
    user_ip = request.headers.get('X-Forwarded-For')

    # get selected reaction
    data = request.get_json()
    reaction_type = data.get('reaction_type')
    
    # check if ip in db 
    existing_ip = CountdownReaction.query.filter_by(ip_countdown_reaction=user_ip).first()

    if not existing_ip:
        #if ip is not in db
        new_vote = CountdownReaction(
            ip_countdown_reaction=user_ip,
            like_countdown=1 if reaction_type == 'like' else 0,
            dislike_countdown=1 if reaction_type == 'dislike' else 0,
            angry_countdown=1 if reaction_type == 'angry' else 0,
            sad_countdown=1 if reaction_type == 'sad' else 0,
            surprised_countdown=1 if reaction_type == 'surprised' else 0,
            denial_countdown=1 if reaction_type == 'denial' else 0
    )
        db.session.add(new_vote)
        countermessage = "Thank you for your contribution."
    else:
        # If the IP is already in the database, take appropriate action
        countermessage = "Your choice is already saved. Thank you."
        
    
    db.session.commit()

    total_like = db.session.query(func.sum(CountdownReaction.like_countdown)).scalar()
    total_like = 0 if total_like is None else total_like
    total_dislike = db.session.query(func.sum(CountdownReaction.dislike_countdown)).scalar()
    total_dislike = 0 if total_dislike is None else total_dislike
    total_sad = db.session.query(func.sum(CountdownReaction.sad_countdown)).scalar()
    total_sad = 0 if total_sad is None else total_sad
    total_angry = db.session.query(func.sum(CountdownReaction.angry_countdown)).scalar()
    total_angry = 0 if total_angry is None else total_angry
    total_denial = db.session.query(func.sum(CountdownReaction.denial_countdown)).scalar()
    total_denial = 0 if total_denial is None else total_denial

    # Return JSON response with updated counts 
    return jsonify({
        'totalLike': total_like,
        'totalDislike': total_dislike,
        'totalSad': total_sad,
        'totalAngry': total_angry,
        'totalDenial': total_denial,
        'countermessage': countermessage
    })



@app.route('/')
def index():
    total_likes = Likes.query.with_entities(func.sum(Likes.likeCount)).scalar()
    countdown = Countdown.query.first()
    remaining_a_time = '0:00:00'
    total_a_loops = 0
    if countdown:
        remaining_a_time = str(timedelta(seconds=countdown.countdown_seconds_a))
        total_a_loops = countdown.total_a
        remaining_b_time = str(timedelta(seconds=countdown.countdown_seconds_b))
        total_b_loops = countdown.total_b
        remaining_c_time = str(timedelta(seconds=countdown.countdown_seconds_c))
        total_c_loops = countdown.total_c
        remaining_d_time = str(timedelta(seconds=countdown.countdown_second_d))
        total_d_loops = countdown.total_d
        remaining_e_time = str(timedelta(seconds=countdown.countdown_second_e))
        total_e_loops = countdown.total_e
        remaining_f_time = str(timedelta(seconds=countdown.countdown_second_f))
        total_f_loops = countdown.total_f
        remaining_g_time = str(timedelta(seconds=countdown.countdown_second_g))
        total_g_loops = countdown.total_g
        remaining_h_time = str(timedelta(seconds=countdown.countdown_second_h))
        total_h_loops = countdown.total_h
        remaining_i_time = str(timedelta(seconds=countdown.countdown_second_i))
        total_i_loops = countdown.total_i
        remaining_j_time = str(timedelta(seconds=countdown.countdown_second_j))
        total_j_loops = countdown.total_j
        remaining_k_time = str(timedelta(seconds=countdown.countdown_second_k))
        total_k_loops = countdown.total_k
        remaining_l_time = str(timedelta(seconds=countdown.countdown_second_l))
        total_l_loops = countdown.total_l
        remaining_m_time = str(timedelta(seconds=countdown.countdown_second_m))
        total_m_loops = countdown.total_m
        
    total_like = db.session.query(func.sum(CountdownReaction.like_countdown)).scalar()
    total_like = 0 if total_like is None else total_like
    total_dislike = db.session.query(func.sum(CountdownReaction.dislike_countdown)).scalar()
    total_dislike = 0 if total_dislike is None else total_dislike
    total_sad = db.session.query(func.sum(CountdownReaction.sad_countdown)).scalar()
    total_sad = 0 if total_sad is None else total_sad
    total_angry = db.session.query(func.sum(CountdownReaction.angry_countdown)).scalar()
    total_angry = 0 if total_angry is None else total_angry
    total_denial = db.session.query(func.sum(CountdownReaction.denial_countdown)).scalar()
    total_denial = 0 if total_denial is None else total_denial



    countermessage = request.args.get('countermessage')


    #print(f"server: remaining time: {remaining_a_time}, Total loops: {total_a_loops}")


    return render_template('index.html', totalLike = total_likes, total_a_loops=total_a_loops, remaining_a_time=remaining_a_time, remaining_b_time=remaining_b_time, total_b_loops=total_b_loops, remaining_c_time=remaining_c_time, total_c_loops=total_c_loops, total_d_loops=total_d_loops, remaining_d_time=remaining_d_time, total_e_loops=total_e_loops, remaining_e_time=remaining_e_time, total_f_loops=total_f_loops, remaining_f_time=remaining_f_time, total_g_loops=total_g_loops, remaining_g_time=remaining_g_time, total_h_loops=total_h_loops, remaining_h_time=remaining_h_time, total_i_loops=total_i_loops, remaining_i_time=remaining_i_time, total_j_loops=total_j_loops, remaining_j_time=remaining_j_time, total_k_loops=total_k_loops, remaining_k_time=remaining_k_time, total_l_loops=total_l_loops, remaining_l_time=remaining_l_time, total_m_loops=total_m_loops, remaining_m_time=remaining_m_time, total_like=total_like, total_dislike=total_dislike, total_sad=total_sad, total_angry=total_angry, total_denial=total_denial, countermessage=countermessage)

@app.route('/countdown-data')
def get_countdown_data():
    countdown = Countdown.query.first()
    if countdown:
        remaining_a_time = str(timedelta(seconds=countdown.countdown_seconds_a))
        total_a_loops = countdown.total_a
        remaining_b_time = str(timedelta(seconds=countdown.countdown_seconds_b))
        total_b_loops = countdown.total_b
        remaining_c_time = str(int(countdown.countdown_seconds_c))
        total_c_loops = countdown.total_c
        remaining_d_time = str(timedelta(seconds=countdown.countdown_second_d))
        total_d_loops = countdown.total_d
        remaining_e_time = str(timedelta(seconds=countdown.countdown_second_e))
        total_e_loops = countdown.total_e
        remaining_f_time = str(timedelta(seconds=countdown.countdown_second_f))
        total_f_loops = countdown.total_f
        remaining_g_time = str(timedelta(seconds=countdown.countdown_second_g))
        total_g_loops = countdown.total_g
        remaining_h_time = str(int(countdown.countdown_second_h))
        total_h_loops = countdown.total_h
        remaining_i_time = str(timedelta(seconds=countdown.countdown_second_i))
        total_i_loops = countdown.total_i
        remaining_j_time = str(timedelta(seconds=countdown.countdown_second_j))
        total_j_loops = countdown.total_j
        remaining_k_time = str(int(countdown.countdown_second_k))
        total_k_loops = countdown.total_k
        remaining_l_time = str(int(countdown.countdown_second_l))
        total_l_loops = countdown.total_l
        remaining_m_time = str(timedelta(seconds=countdown.countdown_second_m))
        total_m_loops = countdown.total_m





        return jsonify({'remaining_time_a': remaining_a_time, 'total_loops_a': total_a_loops, 'remaining_time_b': remaining_b_time, 'total_loops_b': total_b_loops, 'remaining_time_c': remaining_c_time, 'total_loops_c': total_c_loops, 'remaining_time_d': remaining_d_time, 'total_loops_d': total_d_loops, 'remaining_time_e': remaining_e_time, 'total_loops_e': total_e_loops, 'remaining_time_f': remaining_f_time, 'total_loops_f': total_f_loops, 'remaining_time_g': remaining_g_time, 'total_loops_g': total_g_loops, 'remaining_time_h': remaining_h_time, 'total_loops_h': total_h_loops, 'remaining_time_i': remaining_i_time, 'total_loops_i': total_i_loops, 'remaining_time_j': remaining_j_time, 'total_loops_j': total_j_loops, 'remaining_time_k': remaining_k_time, 'total_loops_k': total_k_loops, 'remaining_time_l': remaining_l_time, 'total_loops_l': total_l_loops, 'remaining_time_m': remaining_m_time, 'total_loops_m': total_m_loops})
    else:
        return jsonify({'remaining_time': '0:00:00', 'total_loops': 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    
@app.route('/USACountdownClock', methods=['GET', 'POST'])
def countdown_api():
    countdown_data = get_countdown_data()
    total_like = db.session.query(func.sum(CountdownReaction.like_countdown)).scalar()
    total_like = 0 if total_like is None else total_like
    total_dislike = db.session.query(func.sum(CountdownReaction.dislike_countdown)).scalar()
    total_dislike = 0 if total_dislike is None else total_dislike
    total_sad = db.session.query(func.sum(CountdownReaction.sad_countdown)).scalar()
    total_sad = 0 if total_sad is None else total_sad
    total_angry = db.session.query(func.sum(CountdownReaction.angry_countdown)).scalar()
    total_angry = 0 if total_angry is None else total_angry
    total_denial = db.session.query(func.sum(CountdownReaction.denial_countdown)).scalar()
    total_denial = 0 if total_denial is None else total_denial

    return render_template('USACountdownClock.html', countdown_data=countdown_data, total_like=total_like, total_dislike=total_dislike, total_sad=total_sad, total_angry=total_angry, total_denial=total_denial)