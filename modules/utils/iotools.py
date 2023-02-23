import os as _os
import csv as _csv
import json as _json


def write_header_in_csv(file, fields: list):
    with open(file, 'w', encoding='utf-8-sig', newline='') as csvFile:
        writer = _csv.DictWriter(
            csvFile, fieldnames=fields, delimiter=',', escapechar='\\')

        writer.writeheader()


def append_in_csv(file, data: dict):
    with open(file, 'a', encoding='utf-8-sig', newline='') as csvFile:
        writer = _csv.DictWriter(
            csvFile, fieldnames=data.keys(), delimiter=',', escapechar='\\')

        writer.writerow(data)


def write_in_csv(file, data: dict):
    if not _os.path.isfile(file):
        write_header_in_csv(file, data.keys())
    append_in_csv(file, data)


def save_in_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        _json.dump(data, f, ensure_ascii=False)


def load_from_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = _json.load(f)

    return data
