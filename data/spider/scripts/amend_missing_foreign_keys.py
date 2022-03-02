"""
Check and correct errors in existing datasets.
"""

import collections
import itertools
import json
import shutil
from pathlib import Path


def amend_missing_foreign_keys():
    data_dir = Path(__file__).parents[1]
    table_path = data_dir.joinpath('tables.json')
    tables = []
    with table_path.open(mode='r', encoding='utf-8') as f:
        tables = json.load(f)

    num_foreign_keys_added = 0
    for table in tables:
        c_dict = collections.defaultdict(list)
        for i, c in enumerate(table['column_names_original']):
            c_name = c[1].lower()
            c_dict[c_name].append(i)
        primary_keys = table['primary_keys']
        # print(primary_keys)
        foreign_keys = set([tuple(sorted(x)) for x in table['foreign_keys']])
        for c_name in c_dict:
            if c_name in ['name', 'id', 'code']:
                continue
            if len(c_dict[c_name]) > 1:
                for p, q in itertools.combinations(c_dict[c_name], 2):
                    if p in primary_keys or q in primary_keys:
                        if not (p, q) in foreign_keys:
                            foreign_keys.add((p, q))
                            print('added: {}-{}, {}-{}'.format(p, table['column_names_original'][p],
                                                               q, table['column_names_original'][q]))
                            num_foreign_keys_added += 1
                            # if num_foreign_keys_added % 10 == 0:
                            #     import pdb
                            #     pdb.set_trace()
        foreign_keys = sorted(list(foreign_keys), key=lambda x: x[0])
        table['foreign_keys'] = foreign_keys

    print('{} foreign key pairs added'.format(num_foreign_keys_added))
    shutil.copyfile(table_path, table_path.stem + '.original.json')
    with table_path.open(mode='w') as o_f:
        json.dump(tables, o_f, indent=4)


if __name__ == '__main__':
    amend_missing_foreign_keys()
