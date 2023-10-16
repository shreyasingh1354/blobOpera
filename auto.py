from flask import Flask,render_template
import subprocess


app = Flask(__name__)


@app.route('/run_hand')
def run_hand():
    try:
        # Run the opera.py script using subprocess
        subprocess.run(['python', 'music.py'], check=True)
        return 'motion executed successfully!'
    except Exception as e:
        return f'Error: {str(e)}'
    

@app.route('/run_opera')
def run_opera():
    try:
        # Run the opera.py script using subprocess
        subprocess.run(['python', 'opera.py'], check=True)
        return 'Opera.py executed successfully!'
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
