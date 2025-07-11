from flask import Flask, request, render_template_string
from instagrapi import Client
import os
import time

app = Flask(__name__)
app.debug = True

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram DM Sender</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .container {
            max-width: 500px;
            background-color: #fff;
            padding: 20px;
            margin-top: 50px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
<div class="container">
    <h2 class="mb-4 text-center">Instagram DM Sender</h2>
    <form method="post" enctype="multipart/form-data">
        <div class="mb-3">
            <label>Instagram Username</label>
            <input type="text" name="username" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Instagram Password</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Target Username</label>
            <input type="text" name="target" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Message File (.txt)</label>
            <input type="file" name="message_file" accept=".txt" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Delay (seconds)</label>
            <input type="number" name="delay" class="form-control" required>
        </div>
        <button class="btn btn-primary w-100">Send Messages</button>
    </form>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target_username = request.form['target']
        delay = int(request.form['delay'])
        file = request.files['message_file']

        # Save and read message file
        file_path = 'messages.txt'
        file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            messages = f.read().splitlines()

        try:
            cl = Client()
            cl.login(username, password)
            user_id = cl.user_id_from_username(target_username)

            for msg in messages:
                cl.direct_send(msg, [user_id])
                time.sleep(delay)

            return f"✅ {len(messages)} messages sent to @{target_username}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
