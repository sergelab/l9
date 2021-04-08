import json
import os
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = os.path.join(os.path.dirname(__file__), 'lot9')

SPLIT_SYMBOL = ' '  # '\t'


# API


# Data from API

events = {
    'aaa': {
        'id': 1000,
        'pattern': 'aaa \\d+$',
        'data': [
            {'numbers': '\\d+'}
        ]
    },
    'line number': {
        'id': 1001,  # Идентификатор присваивается при добавлении события
        'pattern': 'line \\d+$',
        'data': [
            {'numbers': '\\d+'}
        ]
    },
    'line number and text': {
        'id': 1002,
        'pattern': 'line \\d+ \\w+',
        'data': [
            {'numbers': '\\d+'},
            {'some_text': '\\w+'},
        ]
    }
}


# ALGO


def find_event(line, dt):
    if not line:
        return

    line = line.replace('\n', '')

    for event in events.values():
        result = re.match(fr'{event["pattern"]}', line)

        if result:
            grp = []
            for d in event.get('data', []):
                for k, v in d.items():
                    grp.append(f'(?P<{k}>{v})')

            tmpl = f"(?P<start>{event['pattern'].split()[0]} {'|'.join(grp)})"
            regex = re.compile(tmpl)

            found = [a.groupdict() for a in regex.finditer(line)]

            # Какие аттрибуты есть у события
            in_attrs = []
            bb = [e for e in event.get('data', [])]
            for b in bb:
                for k, v in b.items():
                    in_attrs.append(k)

            # print('Ready attrs names ', in_attrs)
            # print('Found ', found)

            res_data = {
                'type': event['id'],
                'dateTime': dt.strftime('%Y-%m-%d %H:%M:%S')
            }
            attrs = {}
            for fnd in found:
                for attr, value in fnd.items():
                    if attr in in_attrs and value:
                        attrs.setdefault(attr, value)

            res_data.setdefault('data', attrs)
            return res_data

    return None


def process(fname):
    print(f'Processing {fname}')

    process_date = datetime.now()

    out_fname = os.path.join(BASE_DIR, 'target', os.path.basename(fname))

    with open(out_fname, 'w') as out_file:
        with open(fname, 'r') as in_f:
            test_i = 1

            for line in in_f.readlines():
                if test_i > 10:
                    break

                rs = find_event(line, process_date)
                if rs:
                    # Пишем в выходной файл
                    out_file.write(f'{json.dumps(rs)}\n')
                test_i += 1


def run():
    paths = sorted(Path(os.path.join(BASE_DIR, 'source')).iterdir(), key=os.path.basename)

    for p in paths:
        process(p)
