from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Đưa các route hiện tại vào đây
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/personal_account')
    def account():
        return render_template('PersonalAccountManagement.html')

    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route('/detail_blog')
    def detail_blog():
        return render_template('detail-blog1.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('admins/dashboard.html')

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=8085)
