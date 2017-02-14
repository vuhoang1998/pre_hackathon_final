from flask import Flask,render_template,redirect,url_for,request
import mongoengine
from mongoengine import *
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(APP_ROOT, 'static/images/')
unit = []

connect(
    "pre_hackathon",
    host ="ds159328.mlab.com",
    port= 59328,
    username = "vuhoang98",
    password = "141298",
)

class Flashcard(Document):
    image = StringField()
    word  = StringField()
    meaning = StringField()


class User(Document):
    name     = StringField()
    username = StringField()
    password = StringField()
    cards = ListField(EmbeddedDocumentField("Flashcard"))


app = Flask(__name__)
images_folder = os.path.join(APP_ROOT, 'static/images/')



@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="GET":
        return render_template("homepage.html")
    if request.method == "POST":
        word=request.form["search"]
        print(word)
        search=Flashcard.objects(word=word).first()
        print(search.objects)
        print(search)
        list={
            "word":search.word,
            "image":search.image,
            "meaning":search.meaning
        }
        print(list)
        return render_template("search result.html",word_list=list)


@app.route('/sign')
def sign():
    return render_template("sign.html")



@app.route("/create/<string:id>",methods=["GET","POST"])
def create(id):
    if not os.path.isdir(images_folder) : #neu folder chua duoc khoi tao
        os.mkdir(images_folder) #mkdir = make directory
    if request.method == "GET" :
        return render_template('create.html',id=id)
    if request.method == "POST":
        for image in request.files.getlist('file'):
            image_name = image.filename
            image_dir = "/".join([images_folder, image_name])
            image.save(image_dir)
            imagex = "/".join(["../static/images", image_name])
        wordx = request.form["word"]
        meaningx = request.form["meaning"]
        user = Flashcard(image=imagex, word = wordx , meaning=meaningx)
        user.save()
    return ("Thank you")


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method =="GET" :
        return render_template("signup.html")
    elif request.method == "POST":
        namex     = request.form["Name"]
        usernamex = request.form["userSignUp"]
        passwordx = request.form["SignUpPassw"]
        user = User.objects(username=usernamex).first()
        if user is None:
            user = User(name=namex,username= usernamex, password=passwordx)
            user.save()
        else: render_template("signupx.html")
        return ("Thank You")


@app.route('/signin',methods=["GET","POST"])
def signin():
    if request.method =="GET" :
        return render_template("signin.html")
    elif request.method == "POST":
        usernamex = request.form["userSignIn"]
        passwordx = request.form["SignInPassw"]
        user = User.objects(username=usernamex).first()
        if (user is not None) and (passwordx == user.password):
            return redirect(url_for('id',id=user.id))
        else:
            return render_template("signinx.html")
        print(user)
        # if


@app.route('/home/<string:id>', methods=["GET", "POST"])
def id(id):
    user = User.objects(id=id).first()

    if request.method == "GET":
        return render_template("idhomepage.html",id=id,name=user.name)
    if request.method == "POST":
        word=request.form["search"]
        print(word)
        search=Flashcard.objects(word=word).first()
        print(search.objects)
        print(search)
        list={
            "word":search.word,
            "image":search.image,
            "meaning":search.meaning
        }
        print(list)
        return render_template("search result.html",word_list=list)
@app.route('/learn/<string:id>',methods=["GET","POST"])
def learn(id):
    return render_template('learn.html',id=id,flashcard_list=Flashcard.objects)

if __name__ == '__main__':
    app.run()
