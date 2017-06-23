#coding=utf-8
from flask import Flask, render_template, request, jsonify
import aiml
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText'].encode('utf-8'))

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        #kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.learn("./aiml/cn-startup.xml")
        kernel.respond("load aiml cnask")
        kernel.saveBrain("bot_brain.brn")

    # kernel now ready for use
    while True:
        if message == "quit":
            exit()
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            bot_response = kernel.respond(message.decode('utf8'))
               # print bot_response
            return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(debug=True, host='10.127.1.178', port=15555)
