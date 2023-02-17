from collections import Counter
import gzip

class SeqReads:
    def __init__(self, read_number, meta, sequence, meta2, quality, gc, n):
        self.read_number = read_number
        self.meta = meta
        self.sequence = sequence
        self.meta2 = meta2
        self.quality = quality
        self.gc = gc
        self.n = n

    def __eq__(self, other):
        return self.sequence == other.sequence

    def __hash__(self):
        return hash(self.sequence)


def read_file(file):
    reads_list = []
    read_number = 1
    with open(file, 'r') as f:
        while True:
            try:
                meta, sequence, meta2, quality = next(f).strip(), next(f).strip(), next(f).strip(), next(f).strip()
                gc = (Counter(sequence)['G'] + Counter(sequence)['C']) / len(sequence)
                n = Counter(sequence)['N'] / len(sequence)
                read = SeqReads(read_number, meta, sequence, meta2, quality, gc, n)
                reads_list.append(read)
                read_number += 1
            except StopIteration:
                break
    return reads_list


def read_compressed_file(file):
    reads_list = []
    read_number = 1
    with gzip.open(file, 'rt', encoding='utf8') as f:
        while True:
            try:
                meta, sequence, meta2, quality = next(f).strip(), next(f).strip(), next(f).strip(), next(f).strip()
                gc = (Counter(sequence)['G'] + Counter(sequence)['C']) / len(sequence)
                n = Counter(sequence)['N'] / len(sequence)
                read = SeqReads(read_number, meta, sequence, meta2, quality, gc, n)
                reads_list.append(read)
                read_number += 1
            except StopIteration:
                break
    return reads_list


def reads_summary(reads):
    lengths = Counter(len(read.sequence) for read in reads)
    mean_len = sum(length * count for length, count in lengths.items()) / sum(lengths.values())
    return f'Reads in the file = {len(reads)}: \nReads sequence average length = {round(mean_len)}'


def gc_percentage(reads):
    total_pct_gc = (sum(read.gc for read in reads) / len(reads)) * 100
    return f'\nGC content average = {total_pct_gc:.2f}%\n'


def n_percentage(reads):
    total_pct_n = (sum(read.n for read in reads) / len(reads)) * 100
    num_ns = sum(read.n > 0 for read in reads)
    pct_string = f'Ns per read sequence = {total_pct_n:.2f}%'
    num_string = f'Reads with Ns = {num_ns}'
    return pct_string, num_string


def count_repeats(reads):
    counts = Counter(reads)
    repeats = dict(filter(lambda elem: elem[1] > 1, counts.items()))
    num_repeats = sum(repeats.values()) - len(repeats)
    return f'\nRepeats = {num_repeats}'


def do_it_all():
    file_name = input()
    if '.gz' in file_name:
        all_reads = read_compressed_file(file_name)
    else:
        all_reads = read_file(file_name)
    it_all = [reads_summary(all_reads), count_repeats(all_reads), gc_percentage(all_reads), n_percentage(all_reads)]
    return it_all


archive1 = do_it_all()
archive2 = do_it_all()
archive3 = do_it_all()
print(*archive1)
