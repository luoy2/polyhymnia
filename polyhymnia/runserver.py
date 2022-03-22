from settings import INSTALLED_APPS
from flask import Flask, request
import logging
from importlib import import_module


app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# import blueprint
for installed_app in INSTALLED_APPS:
    bp_name = installed_app + '_bp'
    mod = import_module(f'views.{installed_app}')
    gunicorn_logger.debug(f"register views for app {installed_app}...")
    app.register_blueprint(getattr(mod, bp_name), url_prefix=f"/{installed_app.replace('.', '/')}")

# from interfaces.views.word2vec import word2vec_bp
# app.register_blueprint(word2vec_bp, url_prefix="/word2vec")
# from interfaces.views.fasttext import fasttext_bp
# app.register_blueprint(fasttext_bp, url_prefix="/fasttext")
# from interfaces.views.labeling import labeling_bp
# app.register_blueprint(labeling_bp, url_prefix="/labeling")
# from interfaces.views.policy import policy_bp
# app.register_blueprint(policy_bp, url_prefix="/policy")



gunicorn_logger.info("server ready!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54322)
