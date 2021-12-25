import sqlalchemy as db
from flask import Flask, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)


Session = sessionmaker()
Base = declarative_base()


def mysql_engine():

    username = 'vertilnn_user1'
    password = 'password'
    hostname = '119.18.54.20'
    database = 'vertilnn_smartapp'

    try:
        return create_engine(
            'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
                username,
                password,
                hostname,
                3306,
                database
            )
        )
    except:
        return False


class User(Base):

    __tablename__ = 'smartappuser'

    user_id       = db.Column(db.String(50), primary_key=True)
    user_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(100), nullable=False)
    company_name  = db.Column(db.String(100), nullable=False)
    contact       = db.Column(db.BigInteger, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    updated_on    = db.Column(db.DateTime)


@app.route('/', methods=['get'])
def home():

    return {
        "msg": "success"
    }


@app.route('/login', methods=['post'])
def login():

    data = request.get_json()

    user_id  = data.get('userId')
    password = data.get('userPassword')

    if not all([user_id, password]):
        return make_response(
            res='Request could not be completed',
            code=500,
        )

    Session.configure(bind=mysql_engine())
    session = Session()

    try:
        data = session.query(User) \
                .filter(User.user_id == user_id) \
                    .first()
    except:
        return make_response(
            res='Something went wrong. Please try again',
            code=500,
        )

    if not data:
        return make_response(
            res='Username could not be found.',
            code=500,
        )

    for rec in data:
        if rec.user_password == password:
            return make_response(
                res='Login successful.',
                code=200,
            )

    return make_response(
        res='Something went wrong. Please try again',
        code=500,
    )


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
