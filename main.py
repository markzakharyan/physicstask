import pandas as pd
from math import *
c = 299792458 # m/s

#open input file and parse data into pandas dataframe
events = []
with open("./muons.txt", "r") as input:
    runNum = None
    eventNum = None
    event = None # format of event is [runNum, eventNum, m1, m2]
    m1 = None # format of m1 and m2 is [pt, eta, phi, m]
    m2 = None
    for line in input:
        # parse event
        if line.startswith("Run"):
            runNum = int(line.split("Run ")[1].split(" event")[0])
            eventNum = int(line.split("event ")[1])
        if line.startswith("m1"):
            m1 = [float(i) for i in line.split("pt,eta,phi,m= ")[1].split(" dptinv")[0].split(" ")]
        if line.startswith("m2"):
            m2 = [float(i) for i in line.split("pt,eta,phi,m= ")[1].split(" dptinv")[0].split(" ")]
        
        if eventNum and m1 and m2:
            event = [runNum, eventNum]
            event.extend(m1)
            event.extend(m2)
            events.append(event)
            runNum = None
            eventNum = None
            m1 = None
            m2 = None



#loads data into pandas dataframe
df = pd.DataFrame(events, columns = ['runNum', 'eventNum', 'm1_pt', 'm1_eta', 'm1_phi', 'm1_m', 'm2_pt', 'm2_eta', 'm2_phi', 'm2_m'])
#print(df)



def getLorentzVector_m1(row):
    px_m1 = row['m1_pt']*cos(row['m1_phi'])
    py_m1 = row['m1_pt']*sin(row['m1_phi'])
    pz_m1 = row['m1_pt']*sinh(row['m1_eta'])
    energy_m1 = sqrt(row['m1_pt']**2 + row['m1_m']**2)
    lorentz_vector_m1 = [energy_m1 / c, px_m1, py_m1, pz_m1]

    return lorentz_vector_m1

def getLorentzVector_m2(row):
    px_m2 = row['m2_pt']*cos(row['m2_phi'])
    py_m2 = row['m2_pt']*sin(row['m2_phi'])
    pz_m2 = row['m2_pt']*sinh(row['m2_eta'])
    energy_m2 = sqrt(row['m2_m']**2 + row['m2_pt']**2)
    lorentz_vector_m2 = [energy_m2 / c, px_m2, py_m2, pz_m2]

    return lorentz_vector_m2

def getInvariantMass(row):

    lorentz_vector_m1 = getLorentzVector_m1(row)
    lorentz_vector_m2 = getLorentzVector_m2(row)

    energy_m1 = lorentz_vector_m1[0] * c
    energy_m2 = lorentz_vector_m2[0] * c

    px_m1 = lorentz_vector_m1[1]
    py_m1 = lorentz_vector_m1[2]
    pz_m1 = lorentz_vector_m1[3]

    px_m2 = lorentz_vector_m2[1]
    py_m2 = lorentz_vector_m2[2]
    pz_m2 = lorentz_vector_m2[3]

    invariant_mass = sqrt(row["m1_m"]**2 + row["m2_m"]**2 + 2*(energy_m1*energy_m2 - px_m1*px_m2 - py_m1*py_m2 - pz_m1*pz_m2))

    return invariant_mass



# adds calculated quantities to dataframe as a new column
df["m1_4_vector"] = df.apply(lambda row: getLorentzVector_m1(row), axis=1)
df["m2_4_vector"] = df.apply(lambda row: getLorentzVector_m2(row), axis=1)
df["invariant_mass"] = df.apply(lambda row: getInvariantMass(row), axis=1)

print(df)


# save dataframe

# not sure what format I should print invariant mass to file, so I'm just dumping each collision as a new line in output.txt
# I'm also saving the dataframe to a file for a nicer looking file.

with open("output.txt", "w") as output:
    for row in df.itertuples():
        output.write(str(row.invariant_mass) + "\n")

df.to_csv("output.csv")