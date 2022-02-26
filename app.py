import os
import json
import flask
import ruamel.yaml

languages = ("pl", "uk", "en")

yaml = ruamel.yaml.YAML()
strings = yaml.load(
    open("strings.yaml", mode="r", encoding="utf-8").read()
)

App = flask.Flask(__name__)


@App.route('/')
def get_index():
    for lang in languages:
        flask.url_for('get_language_index', lang=lang)
        flask.url_for('get_language_mapjs', lang=lang)
    return ''


@App.route('/<lang>/index.html')
@App.route('/<lang>/')
def get_language_index(lang):
    for point_id in points:
        flask.url_for('get_point_permalink', lang=lang, point_id=point_id)
    return flask.render_template('index.html', strings=strings, lang=lang)



@App.route('/<lang>/map.js')
def get_language_mapjs(lang):
    flask.url_for('get_osm_data_geojson')
    return (
        flask.render_template('map.js', strings=strings, lang=lang),
        {'Content-Type': 'application/javascript'},
    )


@App.route('/data/osm_data.geojson')
def get_osm_data_geojson():
    if not os.path.exists("osm_data.geojson"):
        return (
            '{"type": "FeatureCollection", "features": []}',
            {'Content-Type': 'application/octet-stream'},
        )
    with open("osm_data.geojson") as file:
        return (
            file.read(),
            {'Content-Type': 'application/octet-stream'},
        )
