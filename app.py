from flask import Flask,render_template,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,ValidationError
import numpy as np

from joblib import dump,load


app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

model = load(open('model.pkl', 'rb'))

@app.route('/', methods=["GET", "POST"])
def home():

    form = InputForm()
    if form.validate_on_submit():
        input_features = []
        parameters = ['glucose', 'blood_pressure', 'insulin', 'bmi', 'age']
        for parameter in parameters:
            input_features.append(request.form.get(parameter))
        final_features = [np.array(input_features)]    
        prediction = model.predict(final_features)
        if prediction[0] == 0:
            text = "You don't have diabetes, nothing to worry!!"
        else:
            text = "You might have diabetes, better get checked!!"    
        return render_template('index.html', form=form, prediction_text=text)
    return render_template('index.html', form=form, prediction_text='')


def numberCheck(form,field):
    
    try:
        int(field.data)
    except ValueError:
        raise ValidationError('This field must be of numeric type')



class InputForm(FlaskForm):

    glucose = StringField('Glucose', validators=[DataRequired(), numberCheck])
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired(), numberCheck])
    insulin = StringField('Insulin', validators=[DataRequired(),numberCheck])
    bmi = StringField('BMI', validators=[DataRequired(),numberCheck])
    age = StringField('Age', validators=[DataRequired(), numberCheck])
    submit = SubmitField('Predict')
