import math


def calculate_distance(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


def calculate_nearby_atom_counts(cnt_bucket, dna_partition, cutoff):
    return sum([
        any([calculate_distance(cnt_atom, dna_atom) < cutoff
             for cnt_atom in cnt_bucket])
        for dna_atom in dna_partition
    ])


def calculate_nearby_atom_counts_by_partitions(cnt_bucket, dna_partitions, cutoff):
    return [calculate_nearby_atom_counts(cnt_bucket, dna_partition, cutoff) for dna_partition in dna_partitions]


def repartition_based_on_definition(bucket, definition):
    max_index = -1
    residue_index_map = {}
    partitions = []
    if definition == 1:
        for elem in bucket:
            if elem[0] not in residue_index_map:
                partitions.append([])
                max_index += 1
                residue_index_map[elem[0]] = max_index
            partitions[max_index].append(elem[1])
    else:
        partitions.append([])
        for elem in bucket:
            partitions[0].append(elem[1])
    return partitions


def calculate_q(cnt_bucket, dna_bucket, cutoff, definition):
    dna_partitions = repartition_based_on_definition(dna_bucket, definition)
    counts = calculate_nearby_atom_counts_by_partitions(cnt_bucket, dna_partitions, cutoff)
    if definition == 1:
        return sum([count > 0 for count in counts]) / len(counts)
    else:
        return counts[0] / len(dna_partitions[0])

