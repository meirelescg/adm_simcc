from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_ind_prod
from ..models.weight import Weights

rest_ind_prod = Blueprint("rest_ind_prod", __name__, url_prefix="/indprod")


@rest_ind_prod.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_insert():
    weights_list = request.get_json()
    if weights_list:
        for weights in weights_list:
            dao_ind_prod.insert_ind_prod(Weights(**weights))
        return jsonify(200, "ok")


@rest_ind_prod.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_delete():
    weight_id = request.args.get("weight_id")
    dao_ind_prod.ind_prod_delete(weight_id)
    return jsonify(200, "ok")


@rest_ind_prod.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_basic_query():
    institution_id = request.args.get("institution_id")
    weights = dao_ind_prod.ind_prod_basic_query(institution_id)
    return jsonify(weights)
