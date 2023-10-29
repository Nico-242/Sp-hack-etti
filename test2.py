from flask import Flask, render_template
import time
import threading

app = Flask(__name__)

a = 0  # Initial value of 'a'

def update_value():
    global a
    while a < 100:
        a += 1
        time.sleep(1)  # Simulating a delay

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def get_update():
    return str(a)

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_value)
    update_thread.start()
    app.run(debug=True)
