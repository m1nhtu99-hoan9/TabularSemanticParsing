""" Download and unzip `spider` dataset """

import requests
import subprocess
import sys
from pathlib import Path

if __name__ == '__main__':
    spider_path = Path(__file__).parents[1]
    spider_zip = spider_path.joinpath('spider.zip')
    url = 'https://drive.google.com/u/1/uc?export=download&confirm=pft3&id=1_AckYkinAnhqmRQtGsQgUKAnTHxxX5J0'

    print("Processing to download 'spider.zip'...")
    if not spider_zip.is_file():
        resp = requests.get(url, allow_redirects=True)
        print(f"Response status: {resp.status_code}")
        with spider_zip.open(mode='wb') as f:
            f.write(resp.content)
    try:
        assert spider_zip.is_file()
    except AssertionError:
        raise FileNotFoundError(f"'spider.zip' not found. Please re-download it.")

    print("Unzipping...")
    try:
        subprocess.check_call(["7z"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Please install 'p7zip-full' OS package, then retry.", file=sys.stderr)
        exit()
    proc_7z = subprocess.Popen(["7z", "x", "-y", str(spider_zip), "-o{}".format(str(spider_zip.parent))],
                               bufsize=64,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
    for line in proc_7z.stdout:
        print(line.strip())
        proc_7z.stdout.flush()
    proc_7z.kill()

    print("Cleanup: Removing 'spider.zip'...")
    spider_zip.unlink(missing_ok=True)
