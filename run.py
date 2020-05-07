"""Run app for debugging
"""

from loris import conn


if __name__ == "__main__":

    conn()

    from loris.app.app import app

    app.run(
        port=1234, debug=False,
        host='0.0.0.0',
        ssl_context=('cert.pem', 'key.pem')
    )
