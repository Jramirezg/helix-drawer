import random
from datetime import datetime


def generate_test_dna_file(output_path, num_entries=500000):
    # Define possible values
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y', 'MT']
    bases = ['A', 'T', 'C', 'G']

    # Header
    header = [
        "#AncestryDNA raw data export",
        f"#Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "#RSID\tCHROMOSOME\tPOSITION\tGENOTYPE"
    ]

    with open(output_path, 'w') as f:
        # Write header
        f.write('\n'.join(header) + '\n')

        # Generate entries
        for _ in range(num_entries):
            chromosome = random.choice(chromosomes)
            position = random.randint(1, 249250621)  # Max length of chromosome 1
            rsid = f"rs{random.randint(1, 999999999)}"
            genotype = random.choice(bases) + random.choice(bases)

            line = f"{rsid}\t{chromosome}\t{position}\t{genotype}\n"
            f.write(line)


if __name__ == "__main__":
    output_file = "large_test_ancestry_data.txt"
    generate_test_dna_file(output_file)
    print(f"Generated test DNA file with 500,000 entries at {output_file}")
