import os

from paste.deploy import loadapp
from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application = loadapp('config:production.ini', relative_to='.')

    serve(application, host='0.0.0.0', port=port)
