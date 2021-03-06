"""Flask application for Complexify."""
import os

from flask import Flask

from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

# .....................................................................................
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)