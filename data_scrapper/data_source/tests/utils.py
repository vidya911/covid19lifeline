import csv
import json


def get_data_from_csv_file(filename):
    json_data = []
    with open(filename, encoding='utf-8') as csvb:
        csv_reader = csv.DictReader(csvb)
        for row in csv_reader:
            json_data.append(row)
    return json_data


def get_data_from_json_file(filename):
    with open(filename, "rb") as fb:
        json_data = json.load(fb)
    return json_data

