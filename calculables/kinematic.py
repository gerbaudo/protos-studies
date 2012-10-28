import supy
import ROOT as r

lvClass = None
def LorentzV(*args) :
    global lvClass
    if lvClass is None : lvClass = r.Math.LorentzVector(r.Math.PxPyPzE4D('float'))
    return lvClass(*args)

class singleP4(supy.wrappedChain.calculable) :
    """
    Calculable to build Lorentz vector for a single particle.
    """
    def __init__(self, collection = None,):
        self.fixes = collection
        self.stash(['px', 'py', 'pz', 'ene'])
    @property
    def name(self) : return '%s%sP4' % self.fixes
    def update(self, _) :
        self.value = LorentzV(self.source[self.px],
                              self.source[self.py],
                              self.source[self.pz],
                              self.source[self.ene])

class P4(supy.wrappedChain.calculable) :
    """
    Calculable to build Lorentz vectors for a collection of particles.
    """
    def __init__(self, collection = None,):
        self.fixes = collection
        self.stash(['px', 'py', 'pz', 'ene'])
    @property
    def name(self) : return '%s%sP4' % self.fixes
    def update(self, _) :
        self.value = [LorentzV(px, py, pz, e) for px,py,pz,e in zip(self.source[self.px],
                                                                    self.source[self.py],
                                                                    self.source[self.pz],
                                                                    self.source[self.ene])]
class TtbarP4(supy.wrappedChain.calculable) :
    "ttbar four momentum"
    def __init__(self, top='top_', antitop='antitop_'):
        self.top = top+'P4'
        self.antitop = antitop+'P4'
    def update(self, _) :
        self.value = self.source[self.top] + self.source[self.antitop]
