import os
import json
import shutil
import hashlib
import datetime as dt
from flask import Flask, request
from werkzeug.utils import secure_filename
from send_mail import send_gmail

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello():
    body = 'None'
    content = None
    ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S Share Information')
    dir_name = get_hash_dir()
    os.mkdir(dir_name)

    if request.form:
        body = [f'{k}: {v}' for k, v in request.form.items()]
        body = '\n'.join(body)
    
    file_names = []
    if request.files:
        for k in request.files:
            fn = secure_filename(f'{request.files[k].filename}')
            fn = os.path.join(dir_name, fn)
            request.files[k].save(fn)
            file_names.append(fn)

    send_gmail(
        sender=os.getenv('USER'),
        password=os.getenv('PASS'),
        send_to=os.getenv('TO'),
        subject=ts,
        body=body,
        file_names=file_names
    )

    shutil.rmtree(dir_name)

    return 'OK\n', 201

def get_hash_dir():
    m = hashlib.sha1()
    m.update(dt.datetime.utcnow().isoformat().encode())
    return m.hexdigest()

if __name__ == "__main__":
    app.run()
