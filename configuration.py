from supy.defaults import *

def mainTree() :
    return ("/","tree")

def leavesToBlackList() :
    return []

def cppROOTDictionariesToGenerate() :
    return [
        #("vector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > >", "vector;Math/LorentzVector.h"),
        #ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > etc. is addressed in linkdef.cxx
        ]

def cppFiles() :
    return [
            "cpp/linkdef.cxx",
            ]
