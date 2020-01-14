#our web app framework!

#you could also generate a skeleton from scratch via
#http://flask-appbuilder.readthedocs.io/en/latest/installation.html

#Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the
#HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine
#for you automatically.
#requests are objects that flask handles (get set post, etc)
from flask import render_template, jsonify, Flask, redirect, url_for, request, flash
#scientific computing library for saving, reading, and resizing images
#from scipy.misc import imsave, imread, imresize
#for matrix math
#import numpy as np
from werkzeug.utils import secure_filename
#for importing our keras model
#import keras.models
#for regular expressions, saves time dealing with string data
import re
import cv2
#system level operations (like loading files)
#import sys
#for reading operating system data
import os
#os.environ['KERAS_BACKEND'] = 'theano'
#import keras
#from keras.models import load_model

#from keras.models import model_from_json
#tell our app where our saved model is
#sys.path.append(os.path.abspath("./model"))
#from load import *
#initalize our flask app
app = Flask(__name__)
app.secret_key = "new year"
#from scipy.misc import imread, imresize,imshow
#global vars for easy reusability
#global model, graph
#initialize these variables
#model, graph = init()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg','jpeg','png']

#decoding an image from base64 into raw representation
def convertImage(imgData1):
	imgstr = re.search(r'base64,(.*)',imgData1).group(1)
	#print(imgstr)
	with open('output.png','wb') as output:
		output.write(imgstr.decode('base64'))


@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

@app.route('/contact/',methods=['GET'])
def contact():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("contact.html")

@app.route('/jsgame/',methods=['GET'])
def jsgame():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("jsgame.html")

@app.route('/about/',methods=['GET'])
def about():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("about.html")

@app.route('/api/sum/<int:num1>/<int:num2>', methods = ['GET'])
def sum(num1,num2):

    return jsonify({'data': num1+num2})

@app.route('/api/sub/<int:num1>/<int:num2>', methods = ['GET'])
def sub(num1,num2):

    return jsonify({'data': num1-num2})


@app.route('/api/mul/<int:num1>/<int:num2>', methods = ['GET'])
def mul(num1,num2):

    return jsonify({'data': num1*num2})

@app.route('/api/div/<int:num1>/<int:num2>', methods = ['GET'])
def div(num1,num2):
    if (num2!=0):
        return jsonify({'data': num1/num2})
    else:
        return jsonify({'data': 'DivisionByZero'})

@app.route('/api/pow/<int:num1>/<int:num2>', methods = ['GET'])
def pow(num1,num2):
        return jsonify({'data': num1**num2})

@app.route('/predictly/',methods=['GET','POST'])
def predictly():
    if request.method == 'POST':
            f = request.files['file']
            name1 = request.values.get("sender")
            name2 = request.values.get("reciever")
            if f.filename=='':
                   flash('No file part')
                   filename = 'Happy-New-Year-2020-PNG-Picture.png'
                   stringy=r'https://qwertyuisub.pythonanywhere.com/newyear?filename='+filename+'&sender='+name1+'&rece='+name2
                   path = os.path.join('static','xrayimgs', filename)
                   return render_template('predictly.html', title='Success', user_image=path ,display_url=stringy)
            if f and allowed_file(f.filename):
                  filename = secure_filename(f.filename)
                  f.save(os.path.join('webapp-api','static', 'xrayimgs', filename))
                  path = os.path.join('static','xrayimgs', filename)
                  #path = 'app/static/xrayimgs/'+filename


                  name1= " ".join(name1.split())
                  name1= name1.replace(' ','_').lower()
                  name2= " ".join(name2.split())
                  name2= name2.replace(' ','_').lower()
                  stringy=r'https://qwertyuisub.pythonanywhere.com/newyear?filename='+filename+'&sender='+name1+'&rece='+name2

                  return render_template('predictly.html', title='Success', user_image=path ,display_url=stringy)
            return render_template('index.html', title='Unsuccessful')
    return render_template('index.html', title='Home')

@app.route('/newyear',methods=['GET'])
def newyear():
    sender=''
    rece=''
    filename = request.args.get('filename')
    path=os.path.join('static','xrayimgs', filename)
    path1=os.path.join('webapp-api','static', 'xrayimgs', filename)
    sender = request.args.get('sender')
    rece = request.args.get('rece')
    if '_' in sender:
        sender=' '.join(sender.split('_'))
    sender = sender.title()
    if '_' in rece:
        rece=' '.join(rece.split('_'))
    rece= rece.title()
    if(os.path.isfile(path1)):
        return render_template('newyear.html', title='Success', send=sender, user_image=path ,recieve=rece)
    else:
        return render_template('newyear.html', title='Success', send=sender, user_image=os.path.join('static','xrayimgs', 'Happy-New-Year-2020-PNG-Picture.png') ,recieve=rece)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 500

if __name__ == "__main__":
	#decide what port to run the app in
	#port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	#app.run(host='0.0.0.0', port=port)
    app.run()
	#optional if we want to run in debugging mode
	#app.run(debug=True)
