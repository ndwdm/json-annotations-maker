# json-annotations-maker
Mark your images with annotations labels for Machine Learning very simply. You can do it locally in your browser.
Inspired by https://github.com/sgp715/simple_image_annotator

INSTALL Flask
$ pip install Flask

RUN
$ python appJson.py /images/train
Open this URL http://127.0.0.1:5000/tagger in your browser, tap on the first point of an object then on another to get bounds of it. Then name the Labels of each object, confirm it by pressing Enter. When all images are marked JSON file will be compiled at appJson.py path.
