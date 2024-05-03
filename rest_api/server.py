from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has a file attached
    if 'file' not in request.files:
        return 'No file attached', 400

    file = request.files['file']

    # Save the file to a desired location
    file.save('uploads/' + file.filename)

    return 'File uploaded successfully', 200

if __name__ == '__main__':
    app.run(host='10.99.94.2', port=5000, debug=True)
