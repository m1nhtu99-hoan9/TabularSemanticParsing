"""
Manually merge `train_spider.json` and `train_others.json`
into `train.json`
"""

import json
from pathlib import Path


if __name__ == '__main__':
    spider_path = Path(__file__).parents[1]
    train_elems = []

    for file_name in ['train_spider.json', 'train_others.json']:
        with spider_path.joinpath(file_name).open(mode='r', encoding='utf-8') as f:
            train_elems.extend(json.load(f))

    with spider_path.joinpath('train.json').open(mode='w', encoding='utf-8') as f:
        json.dump(train_elems, f, indent=4)
