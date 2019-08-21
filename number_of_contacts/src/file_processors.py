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
