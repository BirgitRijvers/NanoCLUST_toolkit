"""
This script combines taxonomic classification results of multiple NanoCLUST runs into 1 CSV file.
"""

import os
import csv
import argparse
from rich import print as rprint

def process_directory(input_directory, output_file, taxonomic_level):
    """
    Checks input directory, reads NanoCLUST output files, and creates a summary CSV file.

    Parameters:
    input_directory (str): The path to the input directory.
    output_file (str): The path to the output CSV file.
    taxonomic_level (str): The taxonomic level to consider.

    Raises:
    FileNotFoundError: If the input directory does not exist or if the expected input file does not exist.
    FileExistsError: If the output file already exists.
    """
    # Check if specified input_directory exists, notify and exit if it doesn't
    if not os.path.exists(input_directory):
        raise FileNotFoundError(f'The input directory {input_directory} does not exist.')    
    # Check if specified output_file exists, notify and exit if it does (don't want to overwrite)
    if os.path.exists(output_file):
        raise FileExistsError(f'The output file {output_file} already exists.')

    # Grab taxonomic level information from taxonomic_code function
    tax = taxonomic_code(taxonomic_level)

    # Create counting variable 
    count=0
    # Open the output summary.csv file for writing
    with open(output_file, 'w', newline='') as output_file:
        output_csv = csv.writer(output_file)
        # Write header
        output_csv.writerow(["runname", "taxid", "rel_abundance"])
        
        # Loop through the subdirectories
        for subdir in os.listdir(input_directory):
            subdir_path = os.path.join(input_directory, subdir)
            
            # Extract name of each run without .fastq
            namelist = subdir.split(".")
            name = str(namelist[0])
            # Check if it's a directory
            if os.path.isdir(subdir_path):
                # Create specific input file path, with taxonomic level and name
                input_file_path = os.path.join(subdir_path, f"{name}", f"rel_abundance_{name}_{tax}.csv")
                
                # Check if input file path exists, notify and exit otherwise
                if not os.path.exists(input_file_path):
                    error_message = (f"\nExpected a file named {input_file_path}. "
                     "Make sure that the input directory you specified contains the direct output directories from NanoCLUST, "
                     "with the classification data output in a folder with the same name as your run.\n")
                    
                    # Clean up if error occured
                    os.remove(output_file.name)

                    # Raise error
                    raise FileNotFoundError(error_message)

                # Create runname and add 1 to count if file path exists
                if os.path.exists(input_file_path):
                    count += 1
                    
                    # Open .csv file to read
                    with open(input_file_path, 'r') as input_file:
                        input_csv = csv.reader(input_file)
                        # Skip header
                        next(input_csv)

                        # Extract abundance information
                        for row in input_csv:
                            taxid, rel_abundance = row
                            output_csv.writerow([name, taxid, rel_abundance])
    
    # Print summary 
    print(f"Processed {count} NanoCLUST output files, and created {output_file.name}")

# Function to create variables for possible taxonomic levels
def taxonomic_code(taxonomic_level):
    """
    Returns the taxonomic 1 letter code for the given taxonomic level.

    Parameters:
    taxonomic_level (str): The taxonomic level ('species', 'genus', 'family', 'order').

    Returns:
    str: The taxonomic code ('S' for species, 'G' for genus, 'F' for family, 'O' for order).
    """
    if taxonomic_level == 'species' or taxonomic_level == 's':
        return 'S'
    elif taxonomic_level == 'genus' or taxonomic_level == 'g':
        return 'G'
    elif taxonomic_level == 'family' or taxonomic_level == 'f':
        return 'F'
    elif taxonomic_level == 'order' or taxonomic_level == 'o':
        return 'O'

# Main function, argparse and excecute process_directory
def main():
    """
    Entry point of the NanoCLUST results summarizer program.
    
    Prints the logo, parses command line arguments, creates an argparse object, and calls the `process_directory` function
    to summarize the NanoCLUST taxonomic classification results from multiple runs.
    """
    title = ("""
         _   _                    ____ _    _   _ ____ _____ 
        | \ | | __ _ _ __   ___  / ___| |  | | | / ___|_   _|
        |  \| |/ _` | '_ \ / _ \| |   | |  | | | \___ \ | |  
        | |\  | (_| | | | | (_) | |___| |__| |_| |___) || |  
        |_| \_|\__,_|_| |_|\___/ \____|_____\___/|____/ |_|                                                                         
            """)
    titleSUMMARIZER= ("""
     ____  _   _ __  __ __  __    _    ____  ___ __________ ____  
    / ___|| | | |  \/  |  \/  |  / \  |  _ \|_ _|__  / ____|  _ \ 
    \___ \| | | | |\/| | |\/| | / _ \ | |_) || |  / /|  _| | |_) |
     ___) | |_| | |  | | |  | |/ ___ \|  _ < | | / /_| |___|  _ < 
    |____/ \___/|_|  |_|_|  |_/_/   \_\_| \_\___/____|_____|_| \_\\
                    """)
    
    # Print pretty ASCII logo and explanation to script
    rprint(f"\n[yellow]Welcome to[/yellow]")
    rprint(f'[green]{title}[magenta]{titleSUMMARIZER}[/green]')
    rprint(f'[blue]This program combines taxonomic classification results of multiple NanoCLUST runs into 1 CSV file.[/blue]\n') 
    
    # Create argparse thingy
    parser = argparse.ArgumentParser(
        prog='NanoCLUST results summarizer',
        description='This program combines taxonomic classification results of multiple NanoCLUST runs into 1 CSV file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Thanks for using this script!'
    )
    
    # Add arguments to parser
    parser.add_argument('input_directory', type=str,
                        help='Path to directory containing the output directories from NanoCLUST')
    parser.add_argument('-o', '--outfile', dest='output_file', type=str,
                        default='./NCsummary.csv',
                        help='Path to output .csv file')
    parser.add_argument('-l', '--level', dest='taxonomic_level', type=str,
                        default='genus',
                        choices=['species', 's', 'genus', 'g', 'family', 'f', 'order', 'o'],
                        help='The taxonomic level you want the classification results summarized of')

    # Parse
    args = parser.parse_args()
    process_directory(args.input_directory, args.output_file, args.taxonomic_level)

# Ensure that main code is only executed when this script runs directly, not when imported as module
if __name__ == "__main__":
    main()
