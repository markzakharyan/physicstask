#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;


// for string delimiter
vector<string> split (string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<string> res;

    while ((pos_end = s.find (delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}

vector<double> convertVector(string line) {
    vector<string> a = split(split(split(line, "pt,eta,phi,m= ")[1], " dptinv")[0], " ");
    vector<double> b;

    for (int i = 0; i < a.size(); i++) {
        b.push_back(stod(a[i]));
    }

    return b;
}


void InvariantMass() {
    
    ifstream is("./muons.txt");
    string line;
    TLorentzVector muon1;
    TLorentzVector muon2;

    TH1F histogram("histogram", "Invariant Mass", 100, 350, 650);

    unique_ptr<TFile> histogram_data( TFile::Open("histogram.root", "RECREATE") );

    while(getline(is, line))
    {
        //printf("%s\n", line.c_str());
        string s1 = "m1";
        string s2 = "m2";


        if (line.substr(0, s1.length()) == s1) {
            vector<double> v = convertVector(line);
            muon1.SetPtEtaPhiM(v[0], v[1], v[2], v[3]);
        }
        if (line.substr(0, s2.length()) == s2) {
            vector<double> v = convertVector(line);
            muon2.SetPtEtaPhiM(v[0], v[1], v[2], v[3]);

            TLorentzVector sum = muon1 + muon2;

            histogram.Fill(sum.M());

            ofstream outputFile;
            outputFile.open("output.txt", ios_base::app);
            outputFile << to_string(sum.M()) << endl;
        }
    }

    histogram_data->WriteObject(&histogram, "histogram");
    histogram_data->Close();

    TFile *histofile = new TFile("histogram.root");
    TH1F *histo = (TH1F*) histofile->Get("histogram");
    histo->Draw();
}