import pickle
import numpy as np
from flask import Flask,request,render_template
import WeatherDataProvider as wdp
import json

app =Flask(__name__)
@app.route('/result',methods=['POST','GET'])
def result():

    temperature = float(request.args.get("temperature"))
    humidity = float(request.args.get("humidity"))
    testdata=np.array([[temperature,humidity]])
    model=pickle.load(open('knnclassifier_2.pkl','rb'))
    pred =model.predict(testdata)
    data={"msg":f"Recommended Crop is {pred[0]}","img":f"static\{pred[0]}.jpg"}
    data = json.dumps(data)
    return data



@app.route('/getweather',methods=['POST','GET'])
def getweather():
    city = request.args.get("cty")
    print("get weather is called")
    data = wdp.fetch_weather_data(city)
    data=json.dumps(data)
    return data


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        if username=='admin' and password=='1234':
            return render_template('crop.html')
        else:
            return render_template('login-index.html',msg='login failed')
    return render_template('login-index.html')


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')

