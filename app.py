from flask import Flask, render_template, request # request is for request parameters
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True # because we're in development, we want to server to keep reloading
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost/funk-travels' # database - change PASSWORD to your own when switching back to dev env
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mfrycanolffhkx:ec0f43f247dc13d49cc5f7f89c2a4a350abcc4227238e4935b19b4bb08a25a6d@ec2-50-17-197-184.compute-1.amazonaws.com:5432/dbv2u0vui2ikbs' # production database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # create database object

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True) # why do we have to limit str char
    agent = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text()) # text is longer

    def __init__(self, customer, agent, rating, comments): # to construct/initialize this model
        self.customer = customer
        self.agent = agent
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST': # why write this condition?
        customer = request.form['customer']
        agent = request.form['agent']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, agent, rating, comments)
        if customer == '' or agent == '':
            return render_template('index.html', message="Please enter required fields")
        # Check if customer does not exist
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            # Add customer data to database
            data = Feedback(customer, agent, rating, comments)
            db.session.add(data)
            db.session.commit() # to put the added data in the database
            send_mail(customer, agent, rating, comments) # SENDS EMAIL to mailtrap
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted feedback")

if __name__ == '__main__':
    app.run()