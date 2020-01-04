from flask import Flask, redirect, render_template, request, url_for
import jobs
import rq
import time


app = Flask(__name__)
jobs.rq.init_app(app)

joblist = []

@app.route('/')
def index():
    l = []
    for job in list(joblist):
        try:
            job.refresh()
        except rq.exceptions.NoSuchJobError:
            joblist.remove(job)
            continue
        l.append({
            'id': job.get_id(),
            'state': job.get_status(),
            'progress': job.meta.get('progress'),
            'result': job.result
            })

    return render_template('index.html', joblist=l)

def scheduledEnqueue():
    job = jobs.callSpotify.queue()
    joblist.append(job)

@app.route('/enqueuejob', methods=['GET', 'POST'])
def enqueuejob():
    job = jobs.callSpotify.queue()
    joblist.append(job)
    return redirect('/')

@app.route('/deletejob', methods=['GET', 'POST'])
def deletejob():
    if request.args.get('jobid'):
        job = rq.job.Job.fetch(request.args.get('jobid'), connection=jobs.rq.connection)
        job.delete()
    return redirect('/')
