import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.config["SECRET_KEY"]=os.getenv("SECRET_KEY","dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL","mysql+pymysql://bugtrack_user:change_me@localhost/bugtrack")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
class User(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(100),nullable=False); email=db.Column(db.String(150),unique=True,nullable=False,index=True); password_hash=db.Column(db.String(255),nullable=False)
class TestCase(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); module=db.Column(db.String(100),nullable=False); steps=db.Column(db.Text,nullable=False); expected_result=db.Column(db.Text,nullable=False); priority=db.Column(db.String(20),default="Medium"); status=db.Column(db.String(20),default="Not Run"); actual_result=db.Column(db.Text,default=""); created_at=db.Column(db.DateTime,default=datetime.utcnow); creator_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
class Bug(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); description=db.Column(db.Text,nullable=False); steps_to_reproduce=db.Column(db.Text,nullable=False); severity=db.Column(db.String(20),default="Medium"); priority=db.Column(db.String(20),default="Medium"); status=db.Column(db.String(30),default="Open"); created_at=db.Column(db.DateTime,default=datetime.utcnow); reporter_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
def login_required(fn):
 @wraps(fn)
 def wrapped(*a,**kw):
  if not session.get("user_id"): flash("Please log in to continue.","warning"); return redirect(url_for("login"))
  return fn(*a,**kw)
 return wrapped
@app.context_processor
def inject_user(): return {"current_user":db.session.get(User,session["user_id"]) if session.get("user_id") else None}
@app.route("/")
def index(): return redirect(url_for("dashboard")) if session.get("user_id") else render_template("index.html")
@app.route("/register",methods=["GET","POST"])
def register():
 if request.method=="POST":
  name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
  if not name or not email or len(password)<8: flash("Enter name and email; password must be at least 8 characters.","danger")
  elif User.query.filter_by(email=email).first(): flash("Email already registered.","danger")
  else:
   u=User(name=name,email=email,password_hash=generate_password_hash(password)); db.session.add(u); db.session.commit(); session.clear(); session["user_id"]=u.id; return redirect(url_for("dashboard"))
 return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
 if request.method=="POST":
  u=User.query.filter_by(email=request.form.get("email","").strip().lower()).first()
  if u and check_password_hash(u.password_hash,request.form.get("password","")): session.clear(); session["user_id"]=u.id; return redirect(url_for("dashboard"))
  flash("Invalid email or password.","danger")
 return render_template("login.html")
@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("index"))
@app.route("/dashboard")
@login_required
def dashboard():
 uid=session["user_id"]; stats={"total":TestCase.query.filter_by(creator_id=uid).count(),"passed":TestCase.query.filter_by(creator_id=uid,status="Pass").count(),"failed":TestCase.query.filter_by(creator_id=uid,status="Fail").count(),"open_bugs":Bug.query.filter_by(reporter_id=uid).filter(Bug.status!="Closed").count()}
 return render_template("dashboard.html",stats=stats,tests=TestCase.query.filter_by(creator_id=uid).all(),bugs=Bug.query.filter_by(reporter_id=uid).all())
@app.route("/tests")
@login_required
def tests():
 q=request.args.get("q","").strip(); query=TestCase.query.filter_by(creator_id=session["user_id"])
 if q: query=query.filter(db.or_(TestCase.title.ilike(f"%{q}%"),TestCase.module.ilike(f"%{q}%")))
 return render_template("tests.html",tests=query.order_by(TestCase.id.desc()).all(),q=q)
@app.route("/tests/new",methods=["GET","POST"])
@login_required
def new_test():
 if request.method=="POST":
  f={k:request.form.get(k,"").strip() for k in ("title","module","steps","expected_result")}
  if not all(f.values()): flash("All fields are required.","danger")
  else:
   t=TestCase(**f,priority=request.form.get("priority","Medium"),creator_id=session["user_id"]); db.session.add(t); db.session.commit(); return redirect(url_for("tests"))
 return render_template("test_form.html")
@app.route("/tests/<int:test_id>/execute",methods=["POST"])
@login_required
def execute_test(test_id):
 t=TestCase.query.filter_by(id=test_id,creator_id=session["user_id"]).first_or_404(); s=request.form.get("status")
 if s not in {"Pass","Fail","Blocked","Not Run"}: abort(400)
 t.status=s; t.actual_result=request.form.get("actual_result",""); db.session.commit(); return redirect(url_for("tests"))
@app.route("/bugs")
@login_required
def bugs():
 q=request.args.get("q","").strip(); query=Bug.query.filter_by(reporter_id=session["user_id"])
 if q: query=query.filter(Bug.title.ilike(f"%{q}%"))
 return render_template("bugs.html",bugs=query.order_by(Bug.id.desc()).all(),q=q)
@app.route("/bugs/new",methods=["GET","POST"])
@login_required
def new_bug():
 if request.method=="POST":
  title=request.form.get("title","").strip(); desc=request.form.get("description","").strip(); steps=request.form.get("steps_to_reproduce","").strip()
  if not all((title,desc,steps)): flash("Title, description and steps are required.","danger")
  else:
   b=Bug(title=title,description=desc,steps_to_reproduce=steps,severity=request.form.get("severity","Medium"),priority=request.form.get("priority","Medium"),reporter_id=session["user_id"]); db.session.add(b); db.session.commit(); return redirect(url_for("bugs"))
 return render_template("bug_form.html")
@app.route("/bugs/<int:bug_id>/status",methods=["POST"])
@login_required
def update_bug_status(bug_id):
 b=Bug.query.filter_by(id=bug_id,reporter_id=session["user_id"]).first_or_404(); s=request.form.get("status")
 if s not in {"Open","In Progress","Fixed","Retest","Closed"}: abort(400)
 b.status=s; db.session.commit(); return redirect(url_for("bugs"))
@app.route("/reports")
@login_required
def reports():
 uid=session["user_id"]; c={s:TestCase.query.filter_by(creator_id=uid,status=s).count() for s in ("Pass","Fail","Blocked","Not Run")}; total=sum(c.values()); c.update(total=total,pass_rate=round(c["Pass"]*100/total,1) if total else 0)
 return render_template("reports.html",counts=c)
@app.cli.command("init-db")
def init_db():
 with app.app_context(): db.create_all()
 print("Database tables created.")
if __name__=="__main__": app.run(debug=os.getenv("FLASK_DEBUG","0")=="1")
