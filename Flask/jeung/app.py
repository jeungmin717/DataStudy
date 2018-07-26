from flask import Flask,render_template
#render template 추가함.

app = Flask(__name__)



@app.route('/') #라우트는 경로를 알려준다 , 주소값에서 슬러시 치면 저 함수를 실행하라 .!
def index():
    # from pandas_ import pandas_index
    # data = pandas_index()
    return render_template('index.html')
    #TODO 나 열심히 할게요


# @app.route('/a') #라우트는 경로를 알려준다 , 주소값에서 슬러시 치면 저 함수를 실행하라 .!
# def hello_world2():
#     return '<h1>A<h1>'
#     #TODO 나 열심히 할게요
#
#
# @app.route('/b')
# def hello_world3():
#     return '<h1>B<h1>'

#변수를 사용함
@app.route('/c/<name>')
def hello_world4(name):
    return '<h1>%s<h1>' %name


#  html  파일명으로 접근하는 방법이 있다.
@app.route('/x/<html>')
def render_world(html=None): # default 값 설정
    return render_template('%s.html'%html)


@app.route('/a/<path>') #다른주소인데 똑같은 파일
@app.route('/<path>')
def render_world2(path=None): # default 값 설정
    if path =='a':
        return render_template('extend.html')
    elif path=='b':
        return render_template("7.10 - ORM Example.html")
    else:
        return render_template('Untitled13.html')

#주소를 입력하면 어떤 결과값을 주느냐.

#사용자한테 어떤 입력을 받아서 어떤값을 줄것인가? : 주소값, 폼 두가지를 내 시스템에서 어떻게 활용할 것인가,
#플라스크는 주소를 받아서 결과를 전달한다.

if __name__ == '__main__':
    app.run(debug=True)
