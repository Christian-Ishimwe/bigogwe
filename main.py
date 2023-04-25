from flask import Flask,url_for,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
this_year=datetime.now().year
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Register(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    tel=db.Column(db.Integer,nullable=False)
    nbr_people=db.Column(db.Integer)
    price=db.Column(db.Float)
    date=db.Column(db.String)
    pin=db.Column(db.Integer)

with app.app_context():
    db.create_all()
    
app.secret_key='christian'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',year=this_year)

@app.route('/register',methods=['POST','GET'])
def register():
        
        if request.method=='POST':
            
            value=int(request.form['num_p'])*25000
            new_tour=Register(
            name=request.form['name'],
            email=request.form['email'],
            tel=request.form['telephy'],
            nbr_people=request.form['num_p'],
            price=value,
            date=request.form['date'],
            pin=request.form['pin']
            )
            flash (f'Book successful reserved for {new_tour.name} !')
            with app.app_context():
                db.session.add(new_tour)
                db.session.commit()
            return redirect(url_for('admin'))
        return render_template('register.html',year=this_year)

@app.route('/admin',methods=['POST','GET'])
def admin():
    useradmin=Register.query.all()
    if request.method=='POST':
        mainadmin=request.form['user']
        mainpin=request.form['pin']
        if mainadmin=='admin@gmail.com' and mainpin=='1234':
            return render_template('all.html', useradmin=useradmin)
        else:
            return render_template('single.html',useradmin=useradmin,mainadmin=mainadmin,mainpin=mainpin)

    return render_template('admin.html',year=this_year)

if __name__=='__main__':
    app.run(debug=True)

