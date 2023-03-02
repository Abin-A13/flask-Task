from flask import request,render_template,flash,redirect,url_for
from .forms import MeetingForm
from . import app
from .utils import generate_token
import requests
import json

meetingdetails = {
                  "topic":" ",  
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "America/Los_Angeles",
                  "agenda": "test",
 
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                }

@app.route('/meeting/',methods=["GET","POST"])
def create_meeting():
    form = MeetingForm()
    if request.method == "POST":
        top= request.form.get('topic')
        dur= request.form.get('duration')
        sttim= request.form.get('start_time')
        ag= request.form.get('agenda')
        meetingdetails["topic"] = top
        meetingdetails["duration"] =dur
        meetingdetails["start_time"] =sttim
        meetingdetails["agenda"] = ag
        headers = {'authorization': 'Bearer ' + generate_token(),
               'content-type': 'application/json'}
        res = requests.post(f'https://api.zoom.us/v2/users/me/meetings',headers=headers, data=json.dumps(meetingdetails))
        data = json.loads(res.text)
        pwd = data.get('password')
        url = data.get('start_url')
        id = data.get('id')
        flash(f'You are sucessfully created meeting, id:{id} your join_link: {url},your password: {pwd}')
        return redirect(url_for('profile'))
    return render_template('createMetting.html',form=form)