from math import *
c = 299792458 # m/s


def getLorentzVector_m1(row):
    px_m1 = row[2]*cos(row[4])
    py_m1 = row[2]*sin(row[4])
    pz_m1 = row[2]*sinh(row[3])
    magnitude_m1_squared = px_m1**2 + py_m1**2 + pz_m1**2
    energy_m1 = sqrt(row[5]**2 + magnitude_m1_squared)
    lorentz_vector_m1 = [energy_m1 / c, px_m1, py_m1, pz_m1]

    return lorentz_vector_m1

def getLorentzVector_m2(row):
    px_m2 = row[6]*cos(row[8])
    py_m2 = row[6]*sin(row[8])
    pz_m2 = row[6]*sinh(row[7])
    magnitude_m2_squared = px_m2**2 + py_m2**2 + pz_m2**2
    energy_m2 = sqrt(row[9]**2 + magnitude_m2_squared)
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

    invariant_mass = sqrt(row[5]**2 + row[9]**2 + 2*(energy_m1*energy_m2 - px_m1*px_m2 - py_m1*py_m2 - pz_m1*pz_m2))

    return invariant_mass

#instantiate output file headers
with open("./output.csv", "w") as output:
    output.writelines('runNum, eventNum, m1_pt, m1_eta, m1_phi, m1_m, m2_pt, m2_eta, m2_phi, m2_m, 4_vector_m1, 4_vector_m2, invariant_mass\n')

# format: 'runNum', 'eventNum', 'm1_pt', 'm1_eta', 'm1_phi', 'm1_m', 'm2_pt', 'm2_eta', 'm2_phi', 'm2_m'
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
            
            lorentz_vector_m1 = getLorentzVector_m1(event)
            lorentz_vector_m2 = getLorentzVector_m2(event)
            invariant_mass = getInvariantMass(event)
            
            with open("./output.txt", "a") as output:
                output.write(str(invariant_mass) + "\n")
            
            event.append("[" + " ".join(str(i) for i in lorentz_vector_m1) + "]")
            event.append("[" + " ".join(str(i) for i in lorentz_vector_m2) + "]")
            event.append(invariant_mass)
            
            with open("./output.csv", "a") as output_csv:
                output_csv.write(",".join(str(i) for i in event) + "\n")
            
            event = []
            runNum = None
            eventNum = None
            m1 = None
            m2 = None








