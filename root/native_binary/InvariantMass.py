from array import array
from ROOT import TFile, TLorentzVector

output_name = "root/native_binary/output_py.txt"
input_name = "root/native_binary/muons.root"

tree = TFile(input_name, "read")

tnt = tree.Get("tnt;1")

with open(output_name, "a") as output:

    # iterate through tnt
    for event in tnt:
        # get the muon objects
        m1 = TLorentzVector()
        m1.SetPtEtaPhiM(event.pt1, event.eta1, event.phi1, 0.1)
        m2 = TLorentzVector()
        m2.SetPtEtaPhiM(event.pt2, event.eta2, event.phi2, 0.1)
        # calculate the invariant mass
        inv_mass = (m1 + m2).M()
        # print the invariant mass
        output.write(str(inv_mass) + "\n")