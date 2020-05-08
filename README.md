# json-annotations-maker
<p>Mark your images with annotations labels for Machine Learning very simply. You can do it locally in your browser.</p>
<p>Inspired by https://github.com/sgp715/simple_image_annotator</p>

<h2>INSTALL Flask</h2>
<p>$ pip install Flask</p>

<h2>RUN</h2>
<p>$ python appJson.py /images/train</p>
<p>Open this URL http://127.0.0.1:5000/tagger in your browser, tap on the first point of an object then on another to get bounds of it. Then name the Labels of each object, confirm it by pressing Enter. When all images are marked JSON file will be compiled at appJson.py path.</p>
