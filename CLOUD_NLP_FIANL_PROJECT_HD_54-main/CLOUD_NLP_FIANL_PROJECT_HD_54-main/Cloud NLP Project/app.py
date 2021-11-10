from botocore.exceptions import ClientError
from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import boto3


app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/sound", methods = ["GET", "POST"])
@cross_origin()
def sound():
    if request.method == "POST":
        text = request.form['texttotranslate']  
        sourcelanguage = request.form['sourcelanguage']
        targetlanguage = request.form['targetlanguage']
        translate = boto3.client(service_name='translate',region_name='us-east-1') 

        result = translate.translate_text(Text=text, SourceLanguageCode=sourcelanguage,TargetLanguageCode=targetlanguage)

        #translated = open("translated.txt","w+")
        #translated.write(str(result["TranslatedText"]))
        text = result['TranslatedText']
        polly = boto3.client(service_name='polly',region_name='us-east-1')  
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',Text=text)
        file = open('static/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        audiospeech=True

    return render_template("index.html",conversion=result['TranslatedText'],audiospeech=audiospeech)


@app.route("/sentiment", methods = ["GET", "POST"])
@cross_origin()
def sentiment():
    if request.method == "POST":
        text = request.form['sentimenttext']  
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

        result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        return render_template("index.html",result=result['Sentiment'])
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
