import argparse
import ujson as json
import matplotlib.pyplot as plt
import numpy as np

from constants import default_cutoff
from file_processors import process_file, process_big_file, process_gro_xtc
from number_of_contacts import calculate_q


def parse_args(*argument_array):
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--input-xtc')
    parser.add_argument('definition', default=1, type=int)
    parser.add_argument('--ignore-h', action='store_true')
    parser.add_argument('--cutoff', type=float, default=default_cutoff)
    return parser.parse_args(*argument_array)


def main(args):
    input_file_name = args.input
    definition = args.definition
    cutoff = args.cutoff
    qs = []
    iterator = process_big_file(input_file_name, args.ignore_h) if not args.input_xtc else process_gro_xtc(input_file_name, args.input_xtc, args.ignore_h)
    for cnt_bucket, dna_bucket in iterator:
        qs.append(calculate_q(cnt_bucket, dna_bucket, cutoff, definition))
    json.dump(qs, open('result', 'w'))
    # cnt_bucket, dna_bucket = process_file(input_file_name, args.ignore_h)
    # print(cutoff, calculate_q(cnt_bucket, dna_bucket, cutoff, definition))
    # cutoff_array = list(np.arange(0.1, 2, 0.05))
    # qs = []
    # for cutoff in cutoff_array:
    #     q = calculate_q(cnt_bucket, dna_bucket, cutoff, definition)
    #     qs.append(q)
    # # derivative_qs = []
    # # for ind in range(2, len(qs)):
    # #     derivative_qs.append((qs[ind] - qs[ind - 2]) / 0.0001)
    # # axes = plt.gca()
    # # axes.set_ylim([0, 1])
    plt.plot(qs, marker='o')
    plt.plot(0.5,linestyle='-')
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.show()


if __name__ == '__main__':
    main(parse_args())
