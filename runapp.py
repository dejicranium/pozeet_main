import os

from paste.deploy import loadapp
from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
<<<<<<< HEAD
    application = loadapp('config:production.ini', relative_to='.')

    serve(application, host='0.0.0.0', port=port)
=======
    app = loadapp('config:production.ini', relative_to='.')

    serve(app, host='0.0.0.0', port=port)
>>>>>>> 983e7c36572509d54a03577a1df1f4fba1e4c334
