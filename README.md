# Brewery
### State-of-the-art ab initio prediction of 1D protein structure annotations 

The web server of Brewery is available at http://distilldeep.ucd.ie/brewery/.  
The train and test sets are available at http://distilldeep.ucd.ie/brewery/data/.

Porter 5 (state-of-the-art SS predictor) is available at http://distilldeep.ucd.ie/porter/.

### Reference
Porter 5: fast, state-of-the-art ab initio prediction of protein secondary structure in 3 and 8 classes<br>
Mirko Torrisi, Manaz Kaleel and Gianluca Pollastri; bioRxiv 289033; doi: https://doi.org/10.1101/289033.


## Setup
```
$ git clone https://github.com/mircare/Brewery/
```

### Requirements
1. Python3 (https://www.python.org/downloads/);
1. NumPy (https://www.scipy.org/scipylib/download.html);
1. HHblits (https://github.com/soedinglab/hh-suite/);
1. uniprot20 (http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz).

#### Optionally (for more accurate predictions):
1. PSI-BLAST (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/); 
1. UniRef90 (ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz).


## How to run Brewery with/without PSI-BLAST
```
# To exploit HHblits only (for fast and accurate predictions)
$ python3 Brewery/Brewery.py -i Brewery/example/2FLGA.fasta --cpu 4 --fast

# To exploit both PSI-BLAST and HHblits (for very accurate predictions)
$ python3 Brewery/Brewery.py -i Brewery/example/2FLGA.fasta --cpu 4
```


## How to visualize the help of Brewery
```
$ python3 Brewery/Porter5.py --help
usage: Brewery.py [-h] [-input fasta_file] [--cpu CPU] [--fast] [--noSS]
                  [--noTA] [--noSA] [--noCD] [--distill] [--setup]

This is the standalone of Brewery5. Run it on a FASTA file to predict its
Secondary Structure in 3- and 8-classes (Porter5), Solvent Accessibility in 4
classes (PaleAle5), Torsional Angles in 14 classes (Porter+5) and Contact
Density in 4 classes (BrownAle).

optional arguments:
  -h, --help         show this help message and exit
  -input fasta_file  FASTA file containing the protein to predict
  --cpu CPU          How many cores to perform this prediction
  --fast             Use only HHblits (skip PSI-BLAST)
  --noSS             Skip Secondary Structure prediction with Porter5
  --noTA             Skip Torsional Angles prediction with Porter+5
  --noSA             Skip Solvent Accessibility prediction with PaleAle5
  --noCD             Skip Contact Density prediction with BrownAle5
  --distill          Generate useful outputs for 3D protein structure
                     prediction
  --setup            Initialize Brewery5 from scratch (it is recommended when
                     there has been any change involving PSI-BLAST, HHblits,
                     Brewery itself, etc).

E.g., run Brewery on 4 cores: python3 Brewery5.py -i example/2FLGA --cpu 4
```


## Performances of Secondary Structure Predictors in 3 classes
| Method | Q3 per AA | SOV'99 per AA | Q3 per protein | SOV'99 per protein |
| :--- | :---: | :---: | :---: | :---: |
| **Brewery** | **83.81%** | **80.41%** | **84.32%** | **81.05%** |
| SPIDER 3 | 83.15% | 79.43% | 83.42% | 79.79% |
| **Brewery *HHblits only*** | **83.06%** | **79.49%** | **83.68%** | **80.26%** |
| SSpro 5 *with templates* | 82.58% | 78.54% | 83.94% | 80.29% |
| PSIPRED 4.01 | 81.88% | 77.36% | 82.48% | 78.22% |
| RaptorX-Property | 81.86% | 78.08% | 82.57% | 78.99% |
| Porter 4 | 81.66% | 78.05% | 82.29% | 78.61% | 
| SSpro5 *ab initio* | 81.17% | 76.87% | 81.10% | 76.92% |
| DeepCNF | 81.04% | 76.74% | 81.16% | 76.99% |

Reference: Table 1 in https://doi.org/10.1101/289033.


## Performances of Secondary Structure Predictors in 8 classes
| Method | Q8 per AA | SOV8_refine per AA | Q8 per protein | SOV8_refine per protein |
| :--- | :---: | :---: | :---: | :---: |
| **Brewery** | **73.02%** | **72.09%** | **73.92%** | **72.64%** |
| SSpro 5 *with templates* | 71.91% | 70.72% | 74.46% | 73.45% |
| **Brewery *HHblits only*** | **71.8%** | **71.16%** | **72.83%** | **71.74%** |
| RaptorX-Property | 70.74% | 69.65% | 71.78% | 70.03% |
| DeepCNF | 69.76% | 68.5% | 70.14% | 68.06% |
| SSpro5 *ab initio* | 68.85% | 67.54% | 69.27% | 67.91% |

Reference: Table 2 in https://doi.org/10.1101/289033.


## Performances of Solvent Accessibility Predictors in up to 4 classes
| Method | Q2 per AA | Q3 per AA | Q4 per AA |
| :--- | :---: | :---: | :---: |
| ACCpro 5 *with templates* | 80.5% | N.A. | N.A. |
| **Brewery** | **80.48%** | **66.41%** | **56.46%** |
| PaleAle 4 | 78.21% | N.A. | 52.53% |
| SPIDER 3 | 77.91% | 61.19% | 49.01% |
| ACCpro 5 *ab initio* | 76.6% | N.A. | N.A. |
| RaptorX-Property | N.A. | 63.25% | N.A. |


## Performances of Torsion Angles Predictors in 14 classes
| Method | Q14 per AA | Q14 per protein |
| :--- | :---: | :---: |
| **Brewery** | **69.93%** | **70.59%** |
| SPIDER 3 | 66.58% | 66.27% |
| Porter+ | 64.73% | 66% |


## Performances of Contact Density Predictors in 4 classes
| Method | Q4 per AA | Q4 per protein |
| :--- | :---: | :---: |
| **Brewery** | **50.01%** | **48%** |
| BrownAle | 46.5% | N.A. |


## License
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

Email us at gianluca[dot]pollastri[at]ucd[dot]ie if you wish to use it for purposes not permitted by the CC BY-NC-SA 4.0.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
