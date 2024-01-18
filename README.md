# NanoCLUST toolkit
Programs that enhance [NanoCLUST](https://github.com/genomicsITER/NanoCLUST) usage and output.

### Scripts included
- NC_runner.py
- NC_summarizer.py

**To be included**
- gridsearch.py (run NanoCLUST on (almost) all combinations of specified parameters)
- summary_to_phyloseq.py (create OTU and TAX files for phyloseq based on CSV summary)
- phyloseqize.py (create OTU and TAX files for phyloseq based directly on NanoCLUST output (no summary needed) (combine with summary_to_phyloseq.py?))
- NC_cluster_concat.py (concatenate cluster consensus sequences from multiple NanoCLUST runs into .fasta file)
- concat_fastqgz.py (recursively concatenate .fastq.gz files in a directory into separate .fastq files) (needed to run NanoCLUST) (combine with NC_runner.py?))

## NC_runner.py
<img width="600" alt="image" src="https://github.com/BirgitRijvers/NanoCLUST_runner/assets/126883391/acb76a00-2832-4ebd-98f6-c0f55e605051">

The [NC_runner.py](https://github.com/BirgitRijvers/NanoCLUST_toolkit/blob/main/NC_runner.py) script streamlines the execution of NanoCLUST on multiple files within a directory using just one command. 

This script is useful when dealing with multiple fastq files, when the approach of using wildcards to select multiple input files does not work. 

### Usage
1. Download the [NC_runner.py](https://github.com/BirgitRijvers/NanoCLUST_runner/blob/main/NC_runner.py) script to a convenient location, preferably your home directory to minimize path-related errors.
2. In the script's argparse default section, provide the **absolute** paths for your database and tax-database to reduce command length and prevent path-related errors.
3. Include the path to the main.nf file from NanoCLUST in the argparse default section.
4. *(Optional)* Modify the default output directory location.
5. *(Optional)* Adjust the default suffix in the argparse section to a suffix you commonly use.
6. Execute the script!

If no input directory is specified or the input directory doesn't exist, the script will exit.

If the specified output directory doesn't exist, the script will notify you and create it.

### Output
NanoCLUST's outputs are organized in the specified output directory or your current working directory by default. For each NanoCLUST run, a separate folder is created with the corresponding sample name. These folders contain three output directories (classification data, FastQC results, and pipeline info) generated by NanoCLUST.

### Example commands
Basic command, only input directory specified (default settings):
```bash
python NC_runner.py sequencedata 
```
Input and output directory, file suffix, main.nf path, database paths specified
```bash
python NC_runner.py sequencedata -o NanoCLUST_out -s .fastq.gz -n project1/programs/NanoCLUST/main.nf -d project1/db/16S_ribosomal_RNA -t project1/db/taxdb
```
Getting help
```bash
python NC_runner.py -h
```
## NC_summarizer.py
The [NC_summarizer.py](https://github.com/BirgitRijvers/NanoCLUST_toolkit/blob/main/NC_summarizer.py) script facilitates the concatenation of taxonomic classification results from multiple NanoCLUST runs into a single CSV file. Users can specify the taxonomic level from which the results should be concatenated.

This script is useful when comparing taxonomic classification results across multiple NanoCLUST runs. Barplots containing relative abundances across samples can be easily created based on the generated CSV.

## Usage
1. Download the [NC_summarizer.py](https://github.com/BirgitRijvers/NanoCLUST_runner/blob/main/NC_summarizer.py) script to a convenient location, preferably your home directory to minimize path-related errors.
2. *(Optional)* Modify the default output directory location in the argparse section of the script.
3. *(Optional)* Modify the default taxonomic level in the argparse section of the script.
4. Execute the script!

## Output
The program generates a single CSV file with three columns: "runname," "taxid," and "rel_abundance." The "runname" column contains the NanoCLUST run name for all taxonomic IDs detected by NanoCLUST, listed in the "taxid" column. The "rel_abundance" column contains the relative abundance of the noted taxid for that run.

### Example commands
Basic command, only input directory specified (default settings):
```bash
python NC_summarizer.py NanoCLUST_out
```
Input directory, output file location and taxonomic level specified
```bash
python NC_summarizer.py NanoCLUST_out -o NanoCLUST_out/NCsummary.csv -l species
```
Getting help
```bash
python NC_summarizer.py -h
```

