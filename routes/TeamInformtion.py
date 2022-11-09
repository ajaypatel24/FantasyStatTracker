import collections
from flask import Blueprint, jsonify, request
import requests
from flask_cors import CORS
from HelperMethods.helper import get_team_map
from Variables.TokenRefresh import oauth, lg
from pytz import timezone
import json
import datetime
from Model.variable import Variable, db
from Variables.TokenRefresh import oauth, lg

TeamInformation = Blueprint("TeamInformation", __name__)
cors = CORS(TeamInformation)


@TeamInformation.route("/team-injury", methods=["GET"])
def get_team_injury_data():
    r = get_team_map()
    res = {}
    tm = list(lg.teams().keys())
    for x in tm:
        team = r[x]
        res[team] = {}
        tm1 = lg.to_team(x).roster()

        for y in tm1:
            if y["status"] != "":
                res[team][y["name"]] = y["status"]

    return res


@TeamInformation.route("/transactions", methods=["GET"])
def get_waiver_pickup():
    res = {}
    r = get_team_map()
    for team in r.values():
        res[team] = {}

    for team in r:
        print(team)

        league_add_drop_information = lg.transactions("add", "")
        for transaction in league_add_drop_information:

            transaction_type = transaction["type"]
            print(transaction_type)
            player_name = ""
            transaction_team_id = ""
            transaction_executed_on_player = ""
            if transaction_type == "add":
                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][0][
                    "destination_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    0
                ]["type"]

            elif transaction_type == "drop":
                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][
                    "source_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    "type"
                ]
            elif transaction_type == "add/drop":  # two transactions, response is weird

                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][0][
                    "destination_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    0
                ]["type"]

                ##############

                full_data_array = transaction["players"]["1"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][
                    "source_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    "type"
                ]

            res[r[transaction_team_id]][player_name] = transaction_executed_on_player

    return jsonify(res)


@TeamInformation.route("/v2/transactions", methods=["GET"])
def get_waiver_pickup_v2():
    res = {}
    r = get_team_map()
    for team in r.values():
        res[team] = {}

    for team in r:
        print(team)

        league_add_drop_information = lg.transactions("add", "")

        for transaction in league_add_drop_information:

            transaction_type = transaction["type"]
            print("checking transaction type", transaction_type == "add/drop")
            timestamp = transaction["timestamp"]
            print(transaction_type)
            player_name = ""
            transaction_team_id = ""
            transaction_executed_on_player = ""
            if transaction_type == "add":
                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][0][
                    "destination_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    0
                ]["type"]

            elif transaction_type == "drop":
                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][
                    "source_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    "type"
                ]

            elif transaction_type == "add/drop":  # two transactions, response is weird

                full_data_array = transaction["players"]["0"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][0][
                    "destination_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    0
                ]["type"]
                res[r[transaction_team_id]][int(timestamp)] = {
                    "transaction": transaction_executed_on_player,
                    "player_name": player_name,
                }
                ##############

                full_data_array = transaction["players"]["1"]["player"]
                player_name = full_data_array[0][2]["name"]["full"]
                transaction_team_id = full_data_array[1]["transaction_data"][
                    "source_team_key"
                ]
                transaction_executed_on_player = full_data_array[1]["transaction_data"][
                    "type"
                ]

            res[r[transaction_team_id]][int(timestamp)] = {
                "transaction": transaction_executed_on_player,
                "player_name": player_name,
            }

    for x in res:
        ra = res[x]
        ra = collections.OrderedDict(sorted(res[x].items(), reverse=True))

    return jsonify(res)


@TeamInformation.route("/v2", methods=["GET"])
def test():
    return jsonify(lg.transactions("add", ""))