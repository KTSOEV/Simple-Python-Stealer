from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    uploaded_file = request.files['archive']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)    
    return 'ok'

if __name__ == '__main__':
    app.run(port=3000)