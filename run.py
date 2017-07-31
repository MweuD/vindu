from app import app
import os



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    if port == 5000:
        app.debug = True

    app.run(host='blooming-sands-23798.herokuapp.com', port=port)
     