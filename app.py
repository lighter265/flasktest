from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    name = db.Column(db.String(255))  # 社員名
    mail = db.Column(db.String(255))  # メール
    is_remote = db.Column(db.Boolean)  # リモート勤務しているか
    is_approve = db.Column(db.Boolean)  # 管理職権限
    department = db.Column(db.String(255))  # 部署
    year = db.Column(db.Integer, default=0)  # 社歴
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

@app.route('/')
def add_page():
	return render_template('index.html')

@app.route('/list')
def index():
	data = ToDo.query.all()
	return render_template('list.html',data=data)

@app.route('/append')
def add__():
	return render_template('append.html')

@app.route('/add', methods=['POST'])
def add():
    form_name = request.form.get('name')  # str
    form_mail = request.form.get('mail')  # str
    # チェックなしならFalse。str -> bool型に変換
    form_is_remote = request.form.get('is_remote', default=False, type=bool)
    form_is_approve = request.form.get('is_approve', default=False, type=bool)
    form_department = request.form.get('department')  # str
    # int, データないとき０
    form_year = request.form.get('year', default=0, type=int)

    employee = ToDo(
        name=form_name,
        mail=form_mail,
        is_remote=form_is_remote,
        is_approve=form_is_approve,
        department=form_department,
        year=form_year
    )
    db.session.add(employee)
    db.session.commit()
    return redirect(url_for('index'))       

@app.route('/del_todo/<int:id>')
def del_todo(id):
	del_data = ToDo.query.filter_by(id=id).first()
	db.session.delete(del_data)
	db.session.commit()
	return redirect(url_for('index'))


if __name__ == '__main__':
    #with app.app_context():
	#    db.create_all()
	app.run()