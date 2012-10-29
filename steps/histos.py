from supy import analysisStep

class DeltaAbsYHisto(analysisStep) :
    def __init__(self, betaMin=None, betaMax=None,
                 absDyVar='DeltaAbsRapidities', betazVar='BoostZ',
                 nbins=40, xmin=-3, xmax=+3) :
        
        hasBm, hasBM = betaMin!=None, betaMax!=None
        for item in ['absDyVar','betazVar','betaMin','betaMax','hasBm','hasBM',
                     'nbins','xmin','xmax'] : setattr(self,item,eval(item))
        self.histoName = "DeltaAbsYHisto"+absDyVar+betazVar
        if hasBm : self.histoName += ("GE%.2f"%betaMin).replace('.','')
        if hasBM : self.histoName += ("LE%.2f"%betaMax).replace('.','')
        self.histoTitle = "%s "%absDyVar
        if hasBm and hasBM : self.histoTitle += "%.2f<|#beta_{z}|<%.2f"%(betaMin,betaMax)
        elif hasBm : self.histoTitle += "%.2f<|#beta_{z}|"%betaMin
        elif hasBM : self.histoTitle += "|#beta_{z}|<%.2f"%betaMax
        self.histoTitle += ";#Delta#||{y};events"
        self.moreName = ""
        if hasBm and hasBM : self.moreName += "%.2f<|beta|<%.2f"%(betaMin,betaMax)
        elif hasBm : self.moreName += "%.2f<|beta|"%(betaMin)
        elif hasBM : self.moreName += "|beta|<%.2f"%(betaMax)
    def uponAcceptance(self,ev) :
        bMin, bMax = self.betaMin, self.betaMax
        dy = ev[self.absDyVar]
        beta = abs(ev[self.betazVar]) if self.hasBm or self.hasBM else None
        betaPass = (self.betaMin < beta if self.hasBm else True) and (self.betaMax > beta if self.hasBM else True)
        if betaPass : self.book.fill(dy, self.histoName, self.nbins, self.xmin, self.xmax, title=self.histoTitle)

