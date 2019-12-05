# Brewery: prediction of 1D protein structure annotations (https://github.com/mircare/Brewery)
# Email us at gianluca[dot]pollastri[at]ucd[dot]ie if you wish to use it for purposes not permitted by the CC BY-NC-SA 4.0.

import argparse, configparser
import os, sys
import time

## check Python version
if sys.version_info[0] < 3:
   print("Python2 detected, please use Python3.")
   exit()

### set argparse
parser = argparse.ArgumentParser(description="This is the standalone of Brewery. Run it on a FASTA file to predict its Secondary Structure in 3- and 8-classes (Porter5), Solvent Accessibility in 4 classes (PaleAle5), Torsional Angles in 14 classes (Porter+5) and Contact Density in 4 classes (BrownAle).",
epilog="E.g., run Brewery on 4 cores: python3 Brewery.py -i example/2FLGA --cpu 4")
parser.add_argument("-input", metavar='fasta_file', type=str, nargs=1, help="FASTA file containing the protein to predict")
parser.add_argument("--cpu", type=int, default=1, help="How many cores to perform this prediction")
parser.add_argument("--fast", help="Use only HHblits (skip PSI-BLAST)", action="store_true")
parser.add_argument("--bfd", help="Harness also the BFD database (https://bfd.mmseqs.com/)", action="store_true")
parser.add_argument("--noSS", help="Skip Secondary Structure prediction with Porter5", action="store_true")
parser.add_argument("--noTA", help="Skip Torsional Angles prediction with Porter+5", action="store_true")
parser.add_argument("--noSA", help="Skip Solvent Accessibility prediction with PaleAle5", action="store_true")
parser.add_argument("--noCD", help="Skip Contact Density prediction with BrownAle5", action="store_true")
parser.add_argument("--distill", help="Generate useful outputs for 3D protein structure prediction", action="store_true")
parser.add_argument("--setup", help="Initialize Brewery from scratch (it is recommended when there has been any change involving PSI-BLAST, HHblits, Brewery itself, etc).", action="store_true")
args = parser.parse_args()

path = os.path.dirname(os.path.abspath(sys.argv[0]))+"/scripts"
## PSI-BLAST and HHblits variables and paths.
config = configparser.ConfigParser()
if not os.path.exists(path+"/config.ini") or args.setup:
    psiblast = input("Please insert the absolute path to psiblast (e.g., /home/username/psiblast): ")
    uniref90 = input("Please insert the absolute path to uniref90 (e.g., /home/username/UniProt/uniref90.fasta): ")
    hhblits = input("Please insert the call to HHblits (e.g., hhblits): ")
    uniprot20 = input("Please insert the absolute path to uniprot20 (e.g., /home/username/uniprot20_2016_02/uniprot20_2016_02): ")
    bfd = input("Please insert the absolute path to BFD (e.g., /home/username/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt): ")
    
    config['DEFAULT'] = {'psiblast': psiblast,
                    'uniref90': uniref90,
                    'hhblits': hhblits,
                    'uniprot20' : uniprot20,
                    'bfd': bfd}

    with open(path+"/config.ini", 'w') as configfile:
        config.write(configfile)

    # compile predict and set absolute paths for all model files
    os.system('cd %s/Predict_BRNN; make -B; cd ..;bash set_models.sh; cd %s' % (path, path))
    
    print("\n>>>>> Setup completed successfully. If any problem, please run \"python3 Brewery.py --setup\". <<<<<\n")
else:
    config.read(path+"/config.ini")

## check arguments
if not args.input:
    print("Usage: python3 "+sys.argv[0]+" -i <fasta_file> [--cpu CPU_cores] [--fast]\n--help to display the help")
    exit()

# save protein path and name, and current PATH
filename = "".join(args.input)
pid = filename#.split(".")[0]#replace(".fasta", "")
predict = path+"/Predict_BRNN/Predict"
models = path+"/Predict_BRNN/models/"


print("~~~~~~~~~ Prediction of "+filename+" started ~~~~~~~~~")

time0 = time.time()
if not args.fast:
    ### run PSI-BLAST and process output
    os.system('%s -query %s -out %s.tmp -out_pssm %s.chk -out_ascii_pssm %s.pssm -save_pssm_after_last_round -num_threads %d -dbsize 0 -num_alignments 300000 -num_iterations 2 -evalue 0.001 -inclusion_ethresh 1e-3 -pseudocount 10 -comp_based_stats 1 -db %s >> %s.log' % (config['DEFAULT']['psiblast'], filename, pid, pid, pid, args.cpu, config['DEFAULT']['uniref90'], pid))
    if not os.path.isfile(pid+".chk"):
        os.system('cp %s.tmp %s.blastpgp' % (pid, pid))
    else:
        os.system('%s -in_pssm %s.chk -out %s.blastpgp -num_threads %d -dbsize 0 -num_alignments 300000 -num_iterations 1 -evalue 0.001 -inclusion_ethresh 1e-3 -comp_based_stats 1 -db %s >> %s.log 2>&1' % (config['DEFAULT']['psiblast'], pid, pid, args.cpu, config['DEFAULT']['uniref90'], pid))
    os.system('%s/process-blast.pl %s.blastpgp %s.flatblast %s' % (path, pid, pid, filename))
    
    time1 = time.time()
    print('PSI-BLAST executed in %.2fs' % (time1-time0))
else:
    time1 = time.time()


### run HHblits and process output
if args.distill:
    os.system('%s -d %s -i %s -opsi %s.psi -diff inf -cpu %d -n 3 -maxfilt 150000 -maxmem 27 -v 2 2>> %s.log >> %s.log' % (config['DEFAULT']['hhblits'], config['DEFAULT']['uniprot20'], filename, pid, args.cpu, pid, pid))
else:
    os.system('%s -d %s -i %s -opsi %s.psi -cpu %d -n 3 -maxfilt 150000 -maxmem 27 -v 2 2>> %s.log >> %s.log' % (config['DEFAULT']['hhblits'], config['DEFAULT']['uniprot20'], filename, pid, args.cpu, pid, pid))
os.system('%s/process-psi.sh %s.psi' % (path, pid))

time2 = time.time()
print('HHblits executed in %.2fs' % (time2-time1))

## harness BFD
if args.bfd:
    time22 = time2
    os.system('%s/reformat.pl psi fas %s.psi %s.fas -v 0' % (path, pid, pid))
    os.system('%s -d %s -i %s.fas -opsi %s_bfd.psi -cpu %d -n 3 -maxfilt 150000 -maxmem 27 -v 2 2>> %s_bfd.log >> %s_bfd.log' % (config['DEFAULT']['hhblits'], config['DEFAULT']['bfd'], filename, pid, args.cpu, pid, pid))
    os.system('%s/process-psi.sh %s_bfd.psi' % (path, pid))

    time2 = time.time()
    print('BFD harnessed in %.2fs' % (time22-time2))


#### encode alignments made with HHblits or PSI-BLAST
os.system('python3 %s/process-alignment.py %s.flatpsi flatpsi %d' % (path, pid, args.cpu)) # generated with HHblits
aa = list("".join(line.strip() for line in open(filename, "r").readlines()[1:])) # get plain list of AA from FASTA
length = len(aa)

flatpsi_ann = open(pid+".flatpsi.ann", "r").readlines()

def concatenate (ann0, ann1, ann01):
    with open(ann01, "w") as out:
        # write header, protein name, and length
        out.write("1\n44 3\n"+ pid +"\n"+ str(length) +"\n")

        # concatenate and write input
        tmp = ann0[4].strip().split(" ")
        tmp0 = ann1[4].split(" ")
        for j in range(length):
            x = j*22
            tmp.insert(x + 22 + j, " ".join(tmp0[x:x+22]))
        out.write(" ".join(tmp))

if not args.fast:
    os.system('python3 %s/process-alignment.py %s.flatblast flatblast %d' % (path, pid, args.cpu)) # generated with PSI-BLAST

    ## concatenate PSI-BLAST and HHblits inputs
    flatblast_ann = open(pid+".flatblast.ann", "r").readlines()
    concatenate(flatblast_ann, flatpsi_ann, pid+".flatblastpsi.ann")
elif not args.bfd:
    # generate fake inputs for models not trained on HHblits inputs
    os.system('cp %s.flatpsi.ann %s.flatblast.ann' % (pid, pid))
    os.system('cp %s.flatpsi.ann %s_bfd.flatpsi.ann' % (pid, pid))
    concatenate(flatpsi_ann, flatpsi_ann, pid+".flatblastpsi.ann")
    os.system('cp %s.flatblastpsi.ann %s.flatpsibfd.ann' % (pid, pid))
    flatblast_ann = flatbfd_ann = open(pid+".flatblast.ann", "r").readlines() # will be used for SS8

# encode BFD alignments and concatenated with HHblits inputs
if args.bfd:
    os.system('python3 %s/process-alignment.py %s_bfd.flatpsi flatpsi %d' % (path, pid, args.cpu)) # generated from BFD

    ## concatenate HHblits and BFD inputs
    flatbfd_ann = open(pid+"_bfd.flatpsi.ann", "r").readlines()
    concatenate(flatpsi_ann, flatbfd_ann, pid+".flatpsibfd.ann")

time3 = time.time()
print('Alignments encoded in %.2fs' % (time3-time2))


###############################################
############     SS prediction     ############
###############################################
if not args.noSS:
    ### predict SS in 3 classes
    os.system('%s %smodelv8_ss3 %s.flatpsi.ann > /dev/null' % (predict, models, pid))
    if not args.fast or not args.bfd:
        os.system('%s %smodelv7_ss3 %s.flatblast.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv78_ss3 %s.flatblastpsi.ann > /dev/null' % (predict, models, pid))
    if args.bfd or args.fast:
        os.system('%s %smodelv8_BFD_ss3 %s_bfd.flatpsi.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv8_HH+BFD_ss3 %s.flatpsibfd.ann > /dev/null' % (predict, models, pid))


    time4 = time.time()
    print('Secondary Structure in 3 classes predicted in %.2fs' % (time4-time3))


    ## ensemble predictions and process output
    toChar = {0 : "H", 1 : "E", 2 : "C"}
    SS = [[0] * 3 for _ in range(length)]
    prediction = open(pid+".ss3", "w")
    prediction.write("#\tAA\tSS\tHelix\tSheet\tCoil\n")

    prob_hh = list(map(float, open(pid+".flatpsi.ann.probsF", "r").readlines()[3].split()))
    if not args.fast or not args.bfd:
        prob_psi = list(map(float, open(pid+".flatblast.ann.probsF", "r").readlines()[3].split()))
        prob_psihh = list(map(float, open(pid+".flatblastpsi.ann.probsF", "r").readlines()[3].split()))
    if args.bfd or args.fast:
        prob_bfd = list(map(float, open(pid+"_bfd.flatpsi.ann.probsF", "r").readlines()[3].split()))
        prob_hhbfd = list(map(float, open(pid+".flatpsibfd.ann.probsF", "r").readlines()[3].split()))

    if not args.fast:
        if args.bfd:
            for i in range(length):
                for j in range(3):
                    SS[i][j] = round((3*prob_psi[i*3+j]+3*prob_hh[i*3+j]+prob_psihh[i*3+j]+3*prob_bfd[i*3+j]+\
                        prob_hhbfd[i*3+j])/11, 4)
        else:
            for i in range(length):
                for j in range(3):
                    SS[i][j] = round((3*prob_psi[i*3+j]+3*prob_hh[i*3+j]+prob_psihh[i*3+j])/7, 4)
    else:
        if args.bfd:
            for i in range(length):
                for j in range(3):
                    SS[i][j] = round((3*prob_hh[i*3+j]+3*prob_bfd[i*3+j]+prob_hhbfd[i*3+j])/7, 4)
        else:
            for i in range(length):
                for j in range(3):
                    SS[i][j] = round((3*prob_psi[i*3+j]+3*prob_hh[i*3+j]+prob_psihh[i*3+j]+3*prob_bfd[i*3+j]+\
                        prob_hhbfd[i*3+j])/11, 4)
    for i in range(length):
        index = SS[i].index(max(SS[i]))
        prediction.write(str(i+1)+"\t"+aa[i]+"\t"+toChar[index]+"\t"+str(SS[i][0])+"\t"+str(SS[i][1])+"\t"+str(SS[i][2])+"\n")
    prediction.flush()


    ######## eight-state prediction ########
    def generate8statesANN(extension, prob, ann):
        input_size = int(ann[1].split()[0])

        ss3 = open(pid+"."+extension+".ann+ss3", "w")
        ss3.write("1\n"+str(input_size+3)+" 8\n"+ pid +"\n"+ str(length) +"\n")

        prob = list(map(str, prob))
        tmp = ann[4].strip().split(" ")

        for j in range(length):
            ss3.write(" ".join(tmp[j*input_size:(j+1)*input_size])+" "+" ".join(prob[j*3:j*3+3])+" ")
        ss3.close()

    ### generate inputs and predict SS8
    generate8statesANN("flatpsi", prob_hh, flatpsi_ann)
    os.system('%s %smodelv8_ss8 %s.flatpsi.ann+ss3 > /dev/null' % (predict, models, pid))
    if not args.fast or not args.bfd:
        generate8statesANN("flatblast", prob_psi, flatblast_ann)

        flatblastpsi_ann = open(pid+".flatblastpsi.ann", "r").readlines()
        generate8statesANN("flatblastpsi", prob_psihh, flatblastpsi_ann)
        os.system('%s %smodelv7_ss8 %s.flatblast.ann+ss3 > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv78_ss8 %s.flatblastpsi.ann+ss3 > /dev/null' % (predict, models, pid))
    if args.bfd or args.fast:
        generate8statesANN("flatbfd", prob_bfd, flatbfd_ann)

        flatpsibfd_ann = open(pid+".flatpsibfd.ann", "r").readlines()
        generate8statesANN("flatpsibfd", prob_hhbfd, flatpsibfd_ann)
        os.system('%s %smodelv8_BFD_ss8 %s.flatbfd.ann+ss3 > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv8_HH+BFD_ss8 %s.flatpsibfd.ann+ss3 > /dev/null' % (predict, models, pid))


    time5 = time.time()
    print('Secondary Structure in 8 classes predicted in %.2fs' % (time5-time4))


    ### ensemble SS predictions and process output
    toChar = {0 : "G", 1 : "H", 2 : "I", 3 : "E", 4 : "B", 5 : "C", 6 : "S", 7 : "T"}
    SS = [[0] * 8 for _ in range(length)]

    prediction = open(pid+".ss8", "w")
    prediction.write("#\tAA\tSS\tG\tH\tI\tE\tB\tC\tS\tT\n")

    prob_hh = list(map(float, open(pid+".flatpsi.ann+ss3.probsF", "r").readlines()[3].split()))
    if not args.fast or not args.bfd:
        prob_psi = list(map(float, open(pid+".flatblast.ann+ss3.probsF", "r").readlines()[3].split()))
        prob_psihh = list(map(float, open(pid+".flatblastpsi.ann+ss3.probsF", "r").readlines()[3].split()))
    if args.bfd or args.fast:
        prob_bfd = list(map(float, open(pid+".flatbfd.ann+ss3.probsF", "r").readlines()[3].split()))
        prob_hhbfd = list(map(float, open(pid+".flatpsibfd.ann+ss3.probsF", "r").readlines()[3].split()))

    if not args.fast:
        if args.bfd:
            for i in range(length):
                for j in range(8):
                    SS[i][j] = round((3*prob_psi[i*8+j]+3*prob_hh[i*8+j]+prob_psihh[i*8+j]+\
                        3*prob_bfd[i*8+j]+prob_hhbfd[i*8+j])/11, 4)
        else:
            for i in range(length):
                for j in range(8):
                    SS[i][j] = round((3*prob_psi[i*8+j]+3*prob_hh[i*8+j]+prob_psihh[i*8+j])/7, 4)
    else:
        if args.bfd:
            for i in range(length):
                for j in range(8):
                    SS[i][j] = round((3*prob_hh[i*8+j]+3*prob_bfd[i*8+j]+prob_hhbfd[i*8+j])/7, 4)
        else:
            for i in range(length):
                for j in range(8):
                    SS[i][j] = round((3*prob_psi[i*8+j]+3*prob_hh[i*8+j]+prob_psihh[i*8+j]+\
                        3*prob_bfd[i*8+j]+prob_hhbfd[i*8+j])/11, 4)
    for i in range(length):
        index = SS[i].index(max(SS[i]))
        prediction.write(str(i+1)+"\t"+aa[i]+"\t"+toChar[index]+"\t"+str(SS[i][0])+"\t"+str(SS[i][1])+"\t"+str(SS[i][2])+\
            "\t"+str(SS[i][3])+"\t"+str(SS[i][4])+"\t"+str(SS[i][5])+"\t"+str(SS[i][6])+"\t"+str(SS[i][7])+"\n")
    prediction.close()


###############################################
############     TA prediction     ############
###############################################
if not args.noTA:
    ### predict TA in 14 classes
    time0TA = time.time()
    classes = 14
    os.system('sed -i "2s|.*|22 14|g" %s.flatpsi.ann' % pid)
    os.system('%s %smodelv8_ta14 %s.flatpsi.ann > /dev/null' % (predict, models, pid))
    if not args.fast or not args.bfd:
        os.system('sed -i "2s|.*|22 14|g" %s.flatblast.ann' % pid)
        os.system('sed -i "2s|.*|44 14|g" %s.flatblastpsi.ann' % pid)
        os.system('%s %smodelv7_ta14 %s.flatblast.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv78_ta14 %s.flatblastpsi.ann > /dev/null' % (predict, models, pid))
    if args.bfd or args.fast:
        os.system('sed -i "2s|.*|22 14|g" %s_bfd.flatpsi.ann' % pid)
        os.system('sed -i "2s|.*|44 14|g" %s.flatpsibfd.ann' % pid)
        os.system('%s %smodelv8_BFD_ta14 %s_bfd.flatpsi.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv8_HH+BFD_ta14 %s.flatpsibfd.ann > /dev/null' % (predict, models, pid))

    print('Torsion Angles in %d classes predicted in %.2fs' % (classes, (time.time()-time0TA)))

    ### ensemble TA predictions and process output
    TA = [[0] * classes for _ in range(length)]
    toChar = {0 : "b", 1 : "h", 2 : "H", 3 : "I", 4 : "C", 5 : "e", 6 : "E", 7 : "S", 8 : "t", 9 : "g", 10 : "T", 11 : "B", 12 : "s", 13 : "i"}

    prediction = open(pid+".ta14", "w")
    prediction.write("#\tAA\tTA\tb\th\tH\tI\tC\te\tE\tS\tt\tg\tT\tB\ts\ti\n")

    prob_hh = list(map(float, open(pid+".flatpsi.ann.probsF", "r").readlines()[3].split()))
    if not args.fast or not args.bfd:
        prob_psi = list(map(float, open(pid+".flatblast.ann.probsF", "r").readlines()[3].split()))
        prob_psihh = list(map(float, open(pid+".flatblastpsi.ann.probsF", "r").readlines()[3].split()))
    if args.bfd or args.fast:
        prob_bfd = list(map(float, open(pid+"_bfd.flatpsi.ann.probsF", "r").readlines()[3].split()))
        prob_hhbfd = list(map(float, open(pid+".flatpsibfd.ann.probsF", "r").readlines()[3].split()))
    
    if not args.fast:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    TA[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/11, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    TA[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j])/7, 4)
    else:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    TA[i][j] = round((3*prob_hh[i*classes+j]+3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/7, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    TA[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/11, 4)
    for i in range(length):
        index = TA[i].index(max(TA[i]))
        prediction.write(str(i+1)+"\t"+aa[i]+"\t"+toChar[index]+"\t"+str(TA[i][0])+"\t"+str(TA[i][1])+"\t"+str(TA[i][2])+\
            "\t"+str(TA[i][3])+"\t"+str(TA[i][4])+"\t"+str(TA[i][5])+"\t"+str(TA[i][6])+"\t"+str(TA[i][7])+"\t"+str(TA[i][8])+
            "\t"+str(TA[i][9])+"\t"+str(TA[i][10])+"\t"+str(TA[i][11])+"\t"+str(TA[i][12])+"\t"+str(TA[i][13])+"\n")
    prediction.close()

 
###############################################
############     SA prediction     ############
###############################################
if not args.noSA:
    ### predict SA in 4 classes
    time0SA = time.time()
    classes = 4
    
    ##add length
    def add_length(filename):
        tmp = open(filename, "r").readlines()
        inputs = int(tmp[1].split()[0])
        tmp[1] = str(inputs+1)+" 4\n"
        ann = tmp[4].split()
        for j in range(int(length)):
            ann.insert((j+1)*inputs + j, str(length/1000))
        tmp[4] = " ".join(ann)
        output = open(filename+"+len", "w")
        for line in tmp:
            output.write("".join(line))
        output.close()

    add_length(pid+".flatpsi.ann")
    os.system('%s %smodelv8_sa4 %s.flatpsi.ann+len > /dev/null' % (predict, models, pid))
    if not args.fast or not args.bfd:
        add_length(pid+".flatblast.ann")
        add_length(pid+".flatblastpsi.ann")
        os.system('%s %smodelv7_sa4 %s.flatblast.ann+len > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv78_sa4 %s.flatblastpsi.ann+len > /dev/null' % (predict, models, pid))
    if args.bfd or args.fast:
        add_length(pid+"_bfd.flatpsi.ann")
        add_length(pid+".flatpsibfd.ann")
        os.system('%s %smodelv8_BFD_sa4 %s_bfd.flatpsi.ann+len > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv8_HH+BFD_sa4 %s.flatpsibfd.ann+len > /dev/null' % (predict, models, pid))        

    print('Solvent Accessibility in %d classes predicted in %.2fs' % (classes, (time.time()-time0SA)))

    ### ensemble SA predictions and process output
    SA = [[0] * classes for _ in range(length)]
    toChar = {0 : "B", 1 : "b", 2 : "e", 3 : "E"}

    prediction = open(pid+".sa4", "w")
    prediction.write("#\tAA\tSA\tB\tb\te\tE\n")

    prob_hh = list(map(float, open(pid+".flatpsi.ann+len.probsF", "r").readlines()[3].split()))
    if not args.fast or not args.bfd:
        prob_psi = list(map(float, open(pid+".flatblast.ann+len.probsF", "r").readlines()[3].split()))
        prob_psihh = list(map(float, open(pid+".flatblastpsi.ann+len.probsF", "r").readlines()[3].split()))
    if args.bfd or args.fast:
        prob_bfd = list(map(float, open(pid+"_bfd.flatpsi.ann+len.probsF", "r").readlines()[3].split()))
        prob_hhbfd = list(map(float, open(pid+".flatpsibfd.ann+len.probsF", "r").readlines()[3].split()))

    if not args.fast:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    SA[i][j] = round((prob_psi[i*classes+j]+prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/5, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    SA[i][j] = round((prob_psi[i*classes+j]+prob_hh[i*classes+j]+prob_psihh[i*classes+j])/3, 4)
    else:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    SA[i][j] = round((prob_hh[i*classes+j]+prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/3, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    SA[i][j] = round((prob_psi[i*classes+j]+prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/5, 4)
    for i in range(length):
        index = SA[i].index(max(SA[i]))
        prediction.write(str(i+1)+"\t"+aa[i]+"\t"+toChar[index]+"\t"+str(SA[i][0])+"\t"+str(SA[i][1])+"\t"+str(SA[i][2])+"\t"+str(SA[i][3])+"\n")
    prediction.close()


###############################################
############     CD prediction     ############
###############################################
if not args.noCD:
    ### predict CD in 4 classes
    time0CD = time.time()
    classes = 4
    os.system('sed -i "2s|.*|22 4|g" %s.flatpsi.ann' % pid)
    os.system('%s %smodelv8_cd4 %s.flatpsi.ann > /dev/null' % (predict, models, pid))
    if not args.fast or not args.bfd:
        os.system('sed -i "2s|.*|22 4|g" %s.flatblast.ann' % pid)
        os.system('sed -i "2s|.*|44 4|g" %s.flatblastpsi.ann' % pid)
        os.system('%s %smodelv7_cd4 %s.flatblast.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv78_cd4 %s.flatblastpsi.ann > /dev/null' % (predict, models, pid))
    if args.bfd or args.fast:
        os.system('sed -i "2s|.*|22 4|g" %s_bfd.flatpsi.ann' % pid)
        os.system('sed -i "2s|.*|44 4|g" %s.flatpsibfd.ann' % pid)
        os.system('%s %smodelv8_BFD_cd4 %s_bfd.flatpsi.ann > /dev/null' % (predict, models, pid))
        os.system('%s %smodelv8_HH+BFD_cd4 %s.flatpsibfd.ann > /dev/null' % (predict, models, pid))

    print('Contact Density in %d classes predicted in %.2fs' % (classes, (time.time()-time0CD)))

    ### ensemble CD predictions and process output
    CD = [[0] * classes for _ in range(length)]
    toChar = {0 : "N", 1 : "n", 2 : "c", 3 : "C"}

    prediction = open(pid+".cd4", "w")
    prediction.write("#\tAA\tCD\tN\tn\tc\tC\n")

    prob_hh = list(map(float, open(pid+".flatpsi.ann.probsF", "r").readlines()[3].split()))
    if not args.fast or not args.bfd:
        prob_psi = list(map(float, open(pid+".flatblast.ann.probsF", "r").readlines()[3].split()))
        prob_psihh = list(map(float, open(pid+".flatblastpsi.ann.probsF", "r").readlines()[3].split()))
    if args.bfd or args.fast:
        prob_bfd = list(map(float, open(pid+"_bfd.flatpsi.ann.probsF", "r").readlines()[3].split()))
        prob_hhbfd = list(map(float, open(pid+".flatpsibfd.ann.probsF", "r").readlines()[3].split()))
        
    if not args.fast:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    CD[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/11, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    CD[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j])/7, 4)
    else:
        if args.bfd:
            for i in range(length):
                for j in range(classes):
                    CD[i][j] = round((3*prob_hh[i*classes+j]+3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/7, 4)
        else:
            for i in range(length):
                for j in range(classes):
                    CD[i][j] = round((3*prob_psi[i*classes+j]+3*prob_hh[i*classes+j]+prob_psihh[i*classes+j]+\
                        3*prob_bfd[i*classes+j]+prob_hhbfd[i*classes+j])/11, 4)
    for i in range(length):
        index = CD[i].index(max(CD[i]))
        prediction.write(str(i+1)+"\t"+aa[i]+"\t"+toChar[index]+"\t"+str(CD[i][0])+"\t"+str(CD[i][1])+"\t"+str(CD[i][2])+"\t"+str(CD[i][3])+"\n")
    prediction.close()

# end
timeEND = time.time()
print('Brewery executed on %s in %.2fs (TOTAL)' % (filename, timeEND-time0))


if args.distill:
    if args.fast: # to guarantee consistency
        os.system('cp %s.flatpsi %s.flatblastpsi' % (pid, pid))
        os.system('mv %s.flatpsi.ann %s.flatblast.ann' % (pid, pid))
    else: # merge flatpsi and flatblast
        os.system('tail -qn +2 %s.flatpsi %s.flatblast | uniq > %s.flatblastpsi; sequences=`wc -l %s.flatblastpsi|awk \'{print $1}\'`; sed -i "1 i $sequences" %s.flatblastpsi' % (pid, pid, pid, pid, pid))
else:
    os.system('rm %s.chk %s.blastpgp %s.flatblast %s.flatblast.ann %s.pssm %s.psi %s.hhr %s.flatpsi 2> /dev/null' % (pid, pid, pid, pid, pid, pid, pid, pid))
    

### remove all the temporary files
os.system('rm %s.flatblastpsi.ann+len.probsF %s.flatblastpsi.ann+len.probs %s.flatblast.ann+len.probsF %s.flatblast.ann+len.probs %s.flatblastpsi.ann+len %s.flatblast.ann+len %s.flatpsi.ann+len.probsF \
%s.flatpsi.ann+len.probs %s.flatpsi.ann+len %s.flatblast.ann+ss3.probs %s.flatpsi.ann.probs %s.flatblast.ann.probs %s.flatblastpsi.ann+ss3.probsF %s.flatblast.ann+ss3 %s.flatblastpsi.ann.probsF \
%s.flatblastpsi.ann %s.flatpsi.ann+ss3.probsF %s.flatpsi.ann %s.flatblastpsi.ann+ss3.probs %s.flatblastpsi.ann+ss3 %s.flatblastpsi.ann.probs %s.flatpsi.ann+ss3.probs %s.flatblast.ann+ss3.probsF \
%s._bfd.flatpsi.ann+len.probs %s_bfd.flatpsi.ann+len.probsF %s_bfd.flatpsi.ann.probs %s_bfd.flatpsi.ann.probsF %s.flatpsibfd.ann+len.probs %s.flatpsibfd.ann+len.probsF %s.flatpsibfd.ann.probs \
%s.flatpsibfd.ann.probsF %s.flatpsi.ann+ss3 %s.flatpsi.ann.probsF %s.flatblast.app %s.flatblast.ann.probsF %s.log %s.tmp 2> /dev/null' % (pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, \
pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid, pid))
