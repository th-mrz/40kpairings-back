import json

from flask import request
from flask_restplus import Namespace, Resource, fields
import pandas as pd
import itertools

api = Namespace('app', 'Pairings endpoints')

pairing_input = api.model('PairingInput', {
    'team': fields.List(fields.String),
    'opponent': fields.List(fields.String),
    'estimates': fields.List(fields.List(fields.Integer))
})

repartition = {
    'VP': fields.Integer,
    'nombre': fields.Integer
}

pairing_output = api.model('PairingOutput', {
    'win': fields.Integer(required=True),
    'loose': fields.Integer(required=True),
    'draw': fields.Integer(required=True),
    'repartition': fields.List(fields.Nested(repartition)),
})

pairing_in = {
    "team": [
        "Drukh", "Orks"
    ],
    "opponent": [
        "Tau", "Necrons"
    ],
    "estimates": [
        [20, 15],
        [0, 10]
    ]
}

pairing_out = {
    'win': 65,
    'loose': 32,
    'draw': 17
}


@api.route('')
class Pairings(Resource):

    @api.doc(body=pairing_input)
    def post(self):
        data = request.get_json()
        df = pd.DataFrame(data["estimates"], index=data["team"], columns=data["opponent"])
        pairing = Pairings.launch_pairing(df)
        result_of = Pairings.result_of(pairing)
        return {
            'win': result_of[0],
            'draw': result_of[1],
            'loose': result_of[2],
            'repartition': json.loads(Pairings.repartition(pairing)),
            'top10': json.loads(Pairings.top_ten(pairing))
        }

    @staticmethod
    def has_duplicates(list_of_elements):
        if len(list_of_elements) == len(set(list_of_elements)):
            return False
        else:
            return True

    @staticmethod
    def sum_score_of_pairing(pairing, df):
        score = 0
        for (x, y) in pairing:
            score += df[x][y]
        return score

    @staticmethod
    def result_of(df):
        win = len(df[df.Estimation > 65].index)
        draw = len(df[(df.Estimation >= 55) & (df.Estimation <= 65)].index)
        loose = len(df[df.Estimation < 55].index)
        return [win, draw, loose]

    @staticmethod
    def top_ten(df):
        return df.sort_values(by="Estimation", ascending=False).head(10).to_json(orient="records")

    @staticmethod
    def repartition(df):
        df = df.Estimation.value_counts().to_frame('count').reset_index().sort_values(by="index")
        df["VP"] = df["index"]
        df["Nombre"] = df["count"]
        return df[["VP", "Nombre"]].sort_values(by="VP").to_json(orient="records")

    @staticmethod
    def launch_pairing(df, paired_estimates=0):
        team1 = df.columns.values.tolist()
        team2 = df.index.values.tolist()
        list_j1 = list(itertools.product([team1[0]], team2))
        list_j2 = list(itertools.product([team1[1]], team2))
        list_j3 = list(itertools.product([team1[2]], team2))
        list_j4 = list(itertools.product([team1[3]], team2))
        list_j5 = list(itertools.product([team1[4]], team2))
        list_j6 = list(itertools.product([team1[5]], team2))
        total = list(itertools.product(list_j1, list_j2, list_j3, list_j4, list_j5, list_j6))
        pairings = filter(lambda pairing: not Pairings.has_duplicates([x[1] for x in pairing]), total)
        list_pairings = list(pairings)
        df_pairings = pd.DataFrame(pd.Series(list_pairings), columns=["Pairings"])
        df_pairings["Estimation"] = df_pairings["Pairings"]\
            .apply(lambda x: Pairings.sum_score_of_pairing(x, df) + paired_estimates)
        return df_pairings
