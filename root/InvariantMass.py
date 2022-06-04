import sys, os
import ROOT, array
from ROOT import TFile, TNtuple, TROOT, TLorentzVector

output_name = "/Users/space/Desktop/task/root/ouput_py.root"
input_name = "/Users/space/Desktop/task/root/muons.txt"
title = "muon collision data"

print('opening file %s ...' % input_name)
with open( input_name, 'r' ) as infile:
    lines  = infile.readlines()

    labels = ["pt", "eta", "phi", "m"]
    
    print(f'writing file {output_name} ...')
    #outfile = TFile( output_name, 'RECREATE', 'ROOT file with an NTuple' )
    ntuple  = TNtuple( 'ntuple', title, ':'.join( labels ) )
    
    currentRun = int(lines[0].split()[1])
    currentEvent = int(lines[0].split()[3])
    print(currentRun)
    print(currentEvent)
    for index, line in enumerate(lines[2:]):
        words = line.split()
        if words[0] == "Run" and words[2] == "event":
            currentRun = int(words[1])
            currentEvent = int(words[3])


        if len(words) > 4:
            #print(words[2:6])
            m1 = TLorentzVector(float(words[2]), float(words[3]), float(words[4]), float(words[5]))
            nextWords = lines[2:][index + 1].split()
            m2 = TLorentzVector(float(nextWords[2]), float(nextWords[3]), float(nextWords[4]), float(nextWords[5]))
            ntuple.Fill(m1,m2)
    
    print(ntuple)
 
print('done')