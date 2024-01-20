"""
This script performs a grid search on the NanoCLUST parameters UMAP set size and minimum cluster size.
"""

import argparse
from itertools import permutations
from subprocess import run

def perform_runs(reads_path, db, taxdb, nf_path, outdir, params):
    """
    Perform runs with different parameters.

    Parameters:
    reads_path (str): Path to the reads.
    db (str): Path to the database.
    taxdb (str): Path to the taxonomic database.
    nf_path (str): Path to the NanoCLUST main.nf file.
    outdir (str): Path to the output directory.
    params (list of int): List of parameters to use for the grid search.
    """
    # Create permutations of the parameters
    perms = permutations(params, 2)

    # Loop over the permutations
    for perm in list(perms):
        umap_size, cluster_size = perm
        # Create command, with umap_size*1000 and cluster_size as parameters
        command = f"nextflow run {nf_path} -profile docker --reads {reads_path} --db {db} --taxdb {taxdb} --outdir {outdir}/U_{umap_size}k_C_{cluster_size} --umap_set_size {umap_size*1000} --min_cluster_size {cluster_size} --polishing_reads {cluster_size}"
        # Run command
        run(command, shell=True)

def main():
    """
    Main function to handle argument parsing and call the perform_runs function.
    """
    # Create argparse thingy
    parser = argparse.ArgumentParser(
        prog='NanoCLUST grid search',
        description='Run NanoCLUST with different parameters.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Thanks for using this script!'
    )
    
    # Add arguments to parser
    parser.add_argument('reads_path', type=str, 
                        help='Path to the reads.')
    parser.add_argument('-o', '--outdir', type=str,
                        default='.', 
                        help='Path to the output directory.')
    parser.add_argument('-p', '--params', nargs='+', type=int, 
                        default=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 400, 600, 800, 1000], 
                        help='List of parameters to use for the grid search.')
    parser.add_argument('-d', '--db', type=str,
                        default='/user/programs/NanoCLUST/db/db', 
                        help='Path to the database.')
    parser.add_argument('-t', '--taxdb', type=str,
                        default='/user/programs/NanoCLUST/db/taxdb',  
                        help='Path to the taxonomic database.')
    parser.add_argument('-n', '--nf_path', type=str,
                        default='programs/NanoCLUST/main.nf',
                        help='Path to the NanoCLUST main.nf file.')

    # Parse!
    args = parser.parse_args()

    # Call the perform_runs function with the parsed arguments
    perform_runs(args.reads_path, args.db, args.taxdb, args.nf_path, args.outdir, args.params)

if __name__ == "__main__":
    main()