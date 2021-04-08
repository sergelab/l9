import json
import os
import re
from datetime import datetime
from pathlib import Path

from events.handler import EventApi

BASE_DIR = os.path.join(os.path.dirname(__file__), 'lot9')


# ALGO


def find_event(events, line, dt):
    if not line:
        return

    line = line.replace('\n', '')

    for event in events.values():
        result = re.match(fr'{event["pattern"]}', line)

        if result:
            grp = []
            for d in event.get('data', []):
                grp.append(f'(?P<{d["name"]}>{d["pattern"]})')

            tmpl = f"(?P<start>{event['pattern'].split()[0]} {'|'.join(grp)})"
            regex = re.compile(tmpl)

            found = [a.groupdict() for a in regex.finditer(line)]

            # Какие аттрибуты есть у события
            in_attrs = []
            bb = [e for e in event.get('data', [])]
            for b in bb:
                in_attrs.append(b['name'])

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


def process(events, fname):
    print(f'Processing {fname}')

    process_date = datetime.now()
    out_fname = os.path.join(BASE_DIR, 'target', os.path.basename(fname))

    with open(out_fname, 'w') as out_file:
        with open(fname, 'r') as in_f:
            test_i = 1

            for line in in_f.readlines():
                if test_i > 10:
                    break

                rs = find_event(events, line, process_date)
                if rs:
                    # Пишем в выходной файл
                    out_file.write(f'{json.dumps(rs)}\n')

                test_i += 1

    print(f'Done')


def run():
    api = EventApi()
    events = {i['name']: i for i in api.get_events().get('events', [])}

    paths = sorted(Path(os.path.join(BASE_DIR, 'source')).iterdir(), key=os.path.basename)

    for p in paths:
        process(events, p)
