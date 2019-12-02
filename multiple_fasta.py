# Brewery: prediction of 1D protein structure annotations (https://github.com/mircare/Brewery)
# Email us at gianluca[dot]pollastri[at]ucd[dot]ie if you wish to use it for purposes not permitted by the CC BY-NC-SA 4.0.

# Usage: python3 multiple_fasta.py -i Fastas/ --cpu 4 --parallel 2
# (run 2 parallel instances of Brewery on 4 cores - total of 8 cores)

import os, sys
import argparse
from multiprocessing import Pool

### parallel code ##
def loop(line):
    os.system('python3 %s -i %s --cpu %d' % (executable, line, args.cpu))

### set argparse
parser = argparse.ArgumentParser(description="This is the standalone of Brewery for multiple inputs. It is sufficient to specify a directory containing FASTA files to start the prediction of the respective structural annotations. It is also possible to run multiple predictions in parallel (TOTAL cpu = --cpu x --parallel).", 
epilog="E.g., to run 2 instances of Brewery on 4 cores (total of 8 cores): python3 multiple_fasta.py -i Fastas/ --cpu 4 --parallel 2")
parser.add_argument("-i", type=str, nargs=1, help="Indicate the directory containing the FASTA files.")
parser.add_argument("--cpu", type=int, default=1, help="Specify how many cores to assign to each prediction.")
parser.add_argument("--parallel", type=int, default=1, help="Specify how many instances to run in parallel.")
parser.add_argument("--fast", help="Use only HHblits (skipping PSI-BLAST) to perform a faster prediction.", action="store_true")
parser.add_argument("--noSS", help="Skip Secondary Structure prediction with Porter5", action="store_true")
parser.add_argument("--noTA", help="Skip Torsional Angles prediction with Porter+5", action="store_true")
parser.add_argument("--noSA", help="Skip Solvent Accessibility prediction with PaleAle5", action="store_true")
parser.add_argument("--noCD", help="Skip Contact Density prediction with BrownAle5", action="store_true")
parser.add_argument("--distill", help="Generate useful outputs for 3D protein structure prediction", action="store_true")
parser.add_argument("--setup", help="Initialize Brewery from scratch. Run it when there has been any change involving PSI-BLAST, HHblits, Brewery itself, etc.", action="store_true")
args = parser.parse_args()

## check arguments
if not args.i:
    print("Usage: python3 "+sys.argv[0]+" -i <fasta_dir> [--cpu CPU_number] [--parallel instances] [--fast]\n--help for the full list of commands")
    exit()

#initialization variables
executable = os.path.abspath(os.path.dirname(sys.argv[0]))+"/Brewery.py"
if not os.path.isfile(executable):
    print("\n---->>No executable retrieved at", executable)
    exit()

if not os.path.isdir("".join(args.i)):
    print("\n---->>","".join(args.i),"isn't a directory! Please consider running split_fasta.py.")
    exit()

if not os.path.isfile(os.path.abspath(os.path.dirname(sys.argv[0]))+"/scripts/config.ini") or args.setup:
    os.system("python3 %s --setup" % executable)

# fetch all the inputs from the passed directory, and sort them by size
os.chdir("".join(args.i))
sorted_files = sorted(os.listdir(os.getcwd()), key = os.path.getsize, reverse=True)

if args.fast:
    sorted_files = [line + " --fast" for line in sorted_files]
if args.noSS:
    sorted_files = [line + " --noSS" for line in sorted_files]
if args.noTA:
    sorted_files = [line + " --noTA" for line in sorted_files]
if args.noSA:
    sorted_files = [line + " --noSA" for line in sorted_files]
if args.noCD:
    sorted_files = [line + " --noCD" for line in sorted_files]
if args.distill:
    sorted_files = [line + " --distill" for line in sorted_files]

#ligth the bomb // launch the parallel code
with Pool(args.parallel) as p:
    p.map(loop, sorted_files, 1)
