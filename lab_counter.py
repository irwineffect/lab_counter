#!/usr/bin/python
import card_reader
import argparse
import time

def read_list(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print "Could not load file: {}".format(filename)
        return list()

    # skip the header
    f.next()
    student_list = list()
    for line in f:
        line = line.rstrip('\n').split(',')
        (student_id, swipe_time) = (line[0], line[1])
        student_list.append((student_id, swipe_time))

    return student_list


def write_list(student_list, filename):
    f = open(filename, "w")
    f.write("id,time\n")
    for i in student_list:
        i = [str(_) for _ in i]
        f.write(",".join(i) + '\n')

    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="csv file to load/save from")
    args = parser.parse_args()

    r = card_reader.card_reader()

    student_list = read_list(args.filename)
    try:
        while True:
            student_id = r.read()
            if student_id is None:
                continue
            print "thanks for swiping!"
            current_time = time.time()
            student_list.append((student_id, current_time))
    except KeyboardInterrupt:
        print "exiting, writing out list..."

    write_list(student_list, args.filename)
    print "goodbye!"

