#!/usr/bin/python
import card_reader
import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="csv file save to")
    args = parser.parse_args()

    r = card_reader.card_reader()

    f = open(args.filename, "a", buffering=1)
    try:
        while True:
            student_id = r.read()
            if student_id is None:
                continue
            print "thanks for swiping!"
            current_time = time.time()
            entry = [student_id, current_time]
            entry = [str(_) for _ in entry]
            f.write(",".join(entry) + '\n')
            f.flush()
    except KeyboardInterrupt:
        print "exiting"
        f.close()

