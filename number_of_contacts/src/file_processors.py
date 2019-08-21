from MDAnalysis.coordinates import XTC
from constants import accept_residues


def process_file(input_file_name, ignore_h):
    cnt_bucket = []
    dna_bucket = []
    with open(input_file_name) as input_file:
        input_file.readline()
        input_file.readline()
        for line in input_file:
            ignore = True
            components = list(filter(lambda x: x != '', line.split(' ')))
            for res in accept_residues:
                if components[0].find(res) != -1:
                    ignore = False
            if ignore or (ignore_h and components[1].find('H') != -1):
                continue
            coordinates = (float(components[3]), float(components[4]), float(components[5]))
            if components[0].find('CNT') != -1:
                cnt_bucket.append(coordinates)
            else:
                dna_bucket.append((components[0], coordinates))
    return cnt_bucket, dna_bucket


def process_big_file(input_file_name, ignore_h):
    with open(input_file_name) as input_file:
        while input_file.readline() != '':
            cnt_bucket = []
            dna_bucket = []
            atoms = int(input_file.readline())
            for _ in range(atoms):
                line = input_file.readline()
                ignore = True
                components = list(filter(lambda x: x != '', line.split(' ')))
                for res in accept_residues:
                    if components[0].find(res) != -1:
                        ignore = False
                if ignore or (ignore_h and components[1].find('H') != -1):
                    continue
                coordinates = (float(components[3]), float(components[4]), float(components[5]))
                if components[0].find('CNT') != -1:
                    cnt_bucket.append(coordinates)
                else:
                    dna_bucket.append((components[0], coordinates))
            input_file.readline()
            yield cnt_bucket, dna_bucket


def process_gro_xtc(gro_file_name, xtc_file_name, ignore_h):
    reader = XTC.XTCReader(xtc_file_name)
    cnt_indx = []
    dna_indx = []
    indx = -1
    with open(gro_file_name) as input_file:
        input_file.readline()
        input_file.readline()
        for line in input_file:
            indx += 1
            ignore = True
            components = list(filter(lambda x: x != '', line.split(' ')))
            for res in accept_residues:
                if components[0].find(res) != -1:
                    ignore = False
            if ignore or (ignore_h and components[1].find('H') != -1):
                continue
            if components[0].find('CNT') != -1:
                cnt_indx.append(indx)
            else:
                dna_indx.append((components[0], indx))

    for timeFrame in reader.trajectory:
        cnt_bucket = []
        dna_bucket = []
        positions = timeFrame.positions / 10
        for cnt in cnt_indx:
            cnt_bucket.append((positions[cnt, 0], positions[cnt, 1], positions[cnt, 2]))
        for res, dna in dna_indx:
            dna_bucket.append((res, (positions[dna, 0], positions[dna, 1], positions[dna, 2])))
        print(timeFrame.time)
        yield cnt_bucket, dna_bucket
