#!/usr/bin/env python

"""
Crawler for https://openclipart.org
"""

import argparse
import re
import requests
import time

def get_url(url, time_out=600):
    r = requests.get(url);
    sleep_time = 1.0;
    while r.status_code != 200:
        print("sleep {}s".format(sleep_time));
        print(url);
        time.sleep(sleep_time);
        r = requests.get(url);
        sleep_time += 2.0;
        if (sleep_time > time_out):
            break;

    if r.status_code != 200:
        print("failed to retrieve {}".format(url));
    else:
        return r;

def parse_clipart_ids(text):
    pattern = "detail/(\d{5,7})";
    matched = re.findall(pattern, text);
    return [int(val) for val in matched];

def get_download_link(clipart_id):
    baseurl = "https://openclipart.org/download/";
    url = "{}/{}/".format(baseurl, clipart_id);
    r = requests.head(url);
    link = r.headers.get("Location", None);
    return link;

def save_records(records):
    output_name = "summary.csv";
    with open(output_name, 'w') as fout:
        fout.write("clipart_id, link\n");
        for entry in records:
            fout.write(",".join([str(v) for v in entry]) + "\n");

def crawl_cliparts(N, out_dir):
    baseurl = "https://openclipart.org/most-popular";

    records = [];
    clipart_ids = set();
    curr_page = 1;
    while len(records) < N:
        url = "{}?page={}".format(baseurl, curr_page);
        contents = get_url(url);
        curr_page += 1;
        if contents is None:
            break;

        for clipart_id in parse_clipart_ids(contents.text):
            if clipart_id in clipart_ids:
                continue;
            print("Clipart id: {}".format(clipart_id));
            clipart_ids.add(clipart_id);

            link = get_download_link(clipart_id);
            records.append([clipart_id, link]);

            if (len(records) > N): break;

            # Sleep a bit to avoid being mistaken as Dos.
            time.sleep(0.5);

        save_records(records);

    return records;

def parse_args():
    parser = argparse.ArgumentParser(__doc__);
    parser.add_argument("--number", "-n", type=int,
            help="How many files to crawl.", default=None);
    parser.add_argument("--output-dir", "-o", help="Output directory",
            default=".");
    return parser.parse_args();

def main():
    args = parse_args();
    records = crawl_cliparts(args.number, args.output_dir);
    save_records(records);

if __name__ == "__main__":
    main();
