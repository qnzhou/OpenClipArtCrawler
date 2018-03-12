#!/usr/bin/env python

"""
Download clip arts stored in summary.csv.
"""

import argparse
import csv
import multiprocessing
import requests
import os
import os.path

def download_clipart(entry):
    clipart_id = entry[0];
    link = entry[1];
    out_dir = entry[2];

    __, ext = os.path.splitext(link);
    out_file = os.path.join(out_dir, "{}{}".format(clipart_id, ext));

    r = None;
    while r is None or r.status_code != 200:
        print("Downloading {}".format(out_file));
        r = requests.get(link, stream=True);
        if r.status_code == 200:
            with open(out_file, 'wb') as fout:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        fout.write(chunk);
        else:
            time.sleep(sleep_time);
            sleep_time += 2.0;
            if sleep_time > 600:
                print("Cannot download {}".format(link));
                break;

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__);
    parser.add_argument("--start", default=None, type=int,
            help="Starting clipart index");
    parser.add_argument("--end", default=None, type=int,
            help="Until clipart index");
    parser.add_argument("--output", "-o", help="Output directory",
            default=".");
    parser.add_argument("summary", help="Summary csv file.");
    return parser.parse_args();

def main():
    args = parse_args();
    pool = multiprocessing.Pool(multiprocessing.cpu_count());
    with open(args.summary, 'r') as fin:
        csv_reader = csv.reader(fin);
        header = next(csv_reader);
        entries = [row + [args.output] for row in csv_reader];

    start = args.start;
    if start is None:
        start = 0;
    end = args.end;
    if end is None:
        end = len(entries);

    pool.map(download_clipart, entries[start:end]);

if __name__ == "__main__":
    main();
