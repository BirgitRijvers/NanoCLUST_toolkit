import os
import subprocess
import argparse
from rich import print as rprint

# Function to run
def run_nanoclust(input_file, output_directory, nanoclust_path, database, tax_database):
    command = f"nextflow run {nanoclust_path} -profile docker --reads {input_file} --db {database} --taxdb {tax_database} --outdir {output_directory}"
    rprint(f"[green]Starting NanoCLUST for {input_file}...[/green]")
    subprocess.run(command, shell=True)

def main():
    title = ("""
     _  _                    ___  _    _   _  ___  _____ 
    | \| | __ _  _ _   ___  / __|| |  | | | |/ __||_   _|
    | .` |/ _` || ' \ / _ \| (__ | |__| |_| |\__ \  | |  
    |_|\_|\__,_||_||_|\___/ \___||____|\___/ |___/  |_|                                                                      
        """)
    titleRUNNER= ("""
             ___  _   _  _  _  _  _  ___  ___              
            | _ \| | | || \| || \| || __|| _ \             
            |   /| |_| || .` || .` || _| |   /             
            |_|_\ \___/ |_|\_||_|\_||___||_|_\  
                """)
    
    # Print pretty logo and explanation to script
    rprint(f"\n[yellow]Welcome to[/yellow]")
    rprint(f'[green]{title}[magenta]{titleRUNNER}[/green]')
    rprint(f'[blue]This script runs NanoCLUST on files in a directory you specify.[/blue]\n')        
    # Create argumentparser
    parser = argparse.ArgumentParser(
        prog='NanoCLUST runner on directory',
        description='This program starts a NanoCLUST run (on default settings) for each passed fastq file in a directory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Thanks for using this script!'
    )

    # Add arguments to parser
    parser.add_argument('input_directory', type=str, 
                        help='Path to directory containing fastq files')
    parser.add_argument('-o', '--outdir', dest='output_directory', type=str, 
                        default='.', 
                        help='Path to output directory')
    parser.add_argument('-s', '--suffix', dest='file_suffix', type=str, 
                        default='pass.fastq', 
                        help='the suffix of all files in the directory that need to be processed')
    parser.add_argument('-n', '--nanoclust', dest='nanoclust_path', type=str, 
                        default='programs/NanoCLUST/main.nf', 
                        help='Path to the NanoCLUST main.nf file')
    parser.add_argument('-d', '--db', dest='database', type=str, 
                        default='/user/programs/NanoCLUST/db/16S_ribosomal_RNA', 
                        help='Absolute path to the database files')
    parser.add_argument('-t', '--taxdb', dest='tax_database', type=str, 
                        default='/user/programs/NanoCLUST/db/taxdb/taxdb', 
                        help='Absolute path to the tax database files')

    # Parse!
    args = parser.parse_args()

    # Check if specified input_directory exists, exit if it doesn't
    if not os.path.exists(args.input_directory):
        rprint(f'[red]Error: The input directory {args.input_directory} does not exist.[/red]')
        exit(1)

    # Check if specified output_directory exists, create it if it doesn't
    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)
        rprint(f'[dark_orange]The output directory {args.output_directory} did not exist, but now it does [/dark_orange][green] :)[/green]\n')

    # Create list with all files from input_directory with correct suffix
    fastqfiles = [filename for filename in os.listdir(args.input_directory) 
                  if filename.endswith(args.file_suffix)]

    # Loop through the files
    for filename in fastqfiles:

        # Run NanoCLUST on each file
        run_nanoclust(
            os.path.join(args.input_directory, filename),
            os.path.join(args.output_directory, filename),
            args.nanoclust_path,
            args.database,
            args.tax_database
        )

# Ensure that main code is only executed when this script runs directly, not when imported as module
if __name__ == "__main__":
    main()
