"""Run app for debugging
"""

import os

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "true"

from loris import conn

if __name__ == "__main__":

    conn()

    from loris.app.app import app

    app.run(
        debug=True,
        port=1236,
        # ssl_context=('cert.pem', 'key.pem')
    )
