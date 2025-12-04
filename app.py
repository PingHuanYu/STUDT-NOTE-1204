from flask import Flask, render_template, request, redirect, url_for
from models import db, Note

app = Flask(__name__)

# 設置資料庫 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 設置路由來顯示所有筆記
@app.route('/')
def index():
    # 查詢資料庫中所有筆記
    notes = Note.query.all()
    # 渲染並返回 index.html，並傳遞筆記資料
    return render_template('index.html', notes=notes)

# 設置路由來顯示新增筆記的表單
@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        # 取得表單資料
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        
        # 創建新的 Note 物件並儲存到資料庫
        new_note = Note(title=title, author=author, content=content)
        db.session.add(new_note)
        db.session.commit()

        # 表單提交後重定向回首頁
        return redirect(url_for('index'))
    
    # 如果是 GET 請求，顯示新增筆記表單
    return render_template('new_note.html')

# 設置主程式入口
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 確保資料表已建立
    app.run(debug=True)