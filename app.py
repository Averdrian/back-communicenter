from flask import Flask
from config import Config


app = Flask(__name__)

app.config.from_object(Config)


print(app.config["PORT"])
print(app.config["DEBUG"])

app.config.port = 8000

print(app.config.port)

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()