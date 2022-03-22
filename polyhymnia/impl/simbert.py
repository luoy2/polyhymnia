from flask import Blueprint, abort
from polyhymnia.decorators.json import *
import logging
from polyhymnia.serializers import NpEncoder
import importlib
from pprint import pformat

simbert_bp = Blueprint('simbert', __name__)
logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')


def allocate_job(job_name, job_params):
    result = {"job": job_name}
    try:
        predictor = importlib.import_module(f"interfaces.predictors.{job_name}")
        predict_result = predictor.predict(**job_params, logger=gunicorn_logger)
        result.update(predict_result)
    except Exception as e:
        gunicorn_logger.error(e, exc_info=True)
        result.update({"result": "failed", "msg": "", "data": {}})
    gunicorn_logger.debug(pformat(result))
    return result


@simbert_bp.route('/submit', methods=['POST'])
@validate_json
@validate_json_param(['jobs', 'shared_params'])
def submit_jobs():
    gunicorn_logger.info("")
    if not request.json:
        abort(400)
    try:
        data = request.json
        jobs = data.get('jobs', [])
        shared_params = data.get('shared_params', {})
        job_results = []
        for job in jobs:
            job_results.append(allocate_job(job, shared_params))
        succeeded = []
        failed = []
        for i in job_results:
            if i['result'] == 'ok':
                succeeded.append(i['job'])
            else:
                failed.append(i['job'])
        gunicorn_logger.info(f"succeeded jobs are: {succeeded}")
        gunicorn_logger.info(f"failed jobs are: {failed}")
        return json.dumps({"status": "ok", "data": job_results}, cls=NpEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e, exc_info=True)
        return jsonify({"status": "failed", "data": {}})
