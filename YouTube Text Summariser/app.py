from flask import Flask, jsonify, make_response, abort, Response
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
from pydantic import BaseModel
from pydantic_webargs import webargs
import urlparse

# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
app.route('/')
def index_page():
    return "Hello world"


app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Get the transcript from the Youtube Transcript API
def transcript(video_id):
    Transc = YouTubeTranscriptApi.get_transcript(video_id)
    strin = ''
    for i in Transc:
        strin = strin+i['text']+' '
    resp = jsonify(Transc)
    resp.status_code = 200

    return strin, resp


def summary(strin):

    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")

    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode(
        "summarize: " + strin, return_tensors="pt", max_length=512, truncation=True)

    # generate the summarization output
    outputs = model.generate(inputs, max_length=150, min_length=40,
                             length_penalty=2.0,  num_beams=4, early_stopping=True)
    resp = Response(js, status=200, mimetype='application/json')
    return tokenizer.decode(outputs[0]), resp


class QueryModel(BaseModel):
    name: str


class BodyModel(BaseModel):
    age: int


@app.route('/[hostname]/api/summarize?youtube_url=<url>', methods=['GET'])
@webargs(query=QueryModel, body=BodyModel)
def get_id(**kwargs):
    #task = [task for task in tasks if task['id'] == task_id]
    url_data = urlparse.urlparse(kwargs)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]

    if len(video_id) == 0:
        abort(404)

    transc, resp = transcript(video_id)
    sum = summary(transc)
    
    return jsonify({'status': resp, "responseText":sum})


# server the app when this file is run
if __name__ == '__main__':

    # using ProxyFisk because Flask is a development server, and this helps fix bugs in the server
    #app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
    #app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run()
