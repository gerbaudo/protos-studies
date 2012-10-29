import calculables, steps, supy, ROOT as r

class basicExample(supy.analysis) :

    def listOfSteps(self,config) :
        shv = supy.steps.histos.value
        shpt, shmass = supy.steps.histos.pt, supy.steps.histos.mass
        shaeta, sheta = supy.steps.histos.absEta, supy.steps.histos.eta
        stepsList = [
            supy.steps.printer.progressPrinter(),
            shv('n_jets',20, 0, 20),
            shv('top_ene',20,0,1e4),
            shpt("top_P4", 100,1,201),
            shpt("jet_P4", 100,1,201, indices = 'Indicesjet_'),
            sheta("top_P4", 100,-10,10),
            sheta("antitop_P4", 100,-10,10),
            shaeta("top_P4", 100,10,10),
            shaeta("antitop_P4", 100,10,10),
            shpt('TtbarP4', 50,0,+0.05e-4),
            shmass('TtbarP4', 100,0,2e3),
            shv('BoostZ',100, -1, +1),
            shv('DeltaAbsRapidities',50, -3, +3),
            ]
        dyh = steps.histos.DeltaAbsYHisto
        stepsList += [dyh()]
        stepsList += [dyh(bm, bM) for bm,bM in [(i*0.2, (i+1)*0.2)
                                                for i in range(int(3./0.2))]]
        return stepsList



# - # list of leaves
# - ['evt_num', 'truth_qqflag',
# -  'n_leptons', 'n_photons', 'n_nonisomu', 'n_jets',
# -  'Wlep_mcid', 'Wlep_px', 'Wlep_py', 'Wlep_pz', 'Wlep_ene',
# -  'Wnu_mcid', 'Wnu_px', 'Wnu_py', 'Wnu_pz', 'Wnu_ene',
# -  'Wquark1_mcid', 'Wquark1_px', 'Wquark1_py', 'Wquark1_pz', 'Wquark1_ene',
# -  'Wquark2_mcid', 'Wquark2_px', 'Wquark2_py', 'Wquark2_pz', 'Wquark2_ene',
# -  'bottom_px', 'bottom_py', 'bottom_pz', 'bottom_ene',
# -  'antibottom_px', 'antibottom_py', 'antibottom_pz', 'antibottom_ene',
# -  'top_px', 'top_py', 'top_pz', 'top_ene',
# -  'antitop_px', 'antitop_py', 'antitop_pz', 'antitop_ene',
# -  'met_px', 'met_py',
# -  # these are vectors
# -  'lep_mcid', 'lep_px', 'lep_py', 'lep_pz', 'lep_ene',
# -  'jet_tag', 'jet_px', 'jet_py', 'jet_pz', 'jet_ene']


    def listOfCalculables(self,config) :
        kin = calculables.kinematic
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ]
                 +[calculables.other.Indices(collection=("jet_",""))]
                 +[kin.P4(collection = ("jet_",""))]
                 +[kin.singleP4(collection = ("top_",""))]
                 +[kin.singleP4(collection = ("antitop_",""))]
                 +[kin.TtbarP4(),
                   kin.AbsSumRapidities(),
                   kin.DeltaAbsRapidities(),]
                 +[kin.BoostZ()]
                 )

    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
        exampleDict.add("SM", '["/tmp/protosSamples/tt-SM.B.root"]',   xs = 1.0e+5 ) # pb
        exampleDict.add("A2", '["/tmp/protosSamples/tt-A2.B.root"]',   xs = 1.0e+5 ) # pb
        exampleDict.add("A4", '["/tmp/protosSamples/tt-A4.B.root"]',   xs = 1.0e+5 ) # pb
        exampleDict.add("A6", '["/tmp/protosSamples/tt-A6.B.root"]',   xs = 1.0e+5 ) # pb
        exampleDict.add("P3", '["/tmp/protosSamples/tt-P3.B.root"]',   xs = 1.0e+5 ) # pb
        return [exampleDict]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 10000 if test else None

        return (
            supy.samples.specify(names = "SM", nEventsMax=nEventsMax, color = r.kBlack, markerStyle = 20)
            + supy.samples.specify(names="A2", nEventsMax=nEventsMax, color = r.kRed)
            + supy.samples.specify(names="A4", nEventsMax=nEventsMax, color = r.kGreen)
            + supy.samples.specify(names="A6", nEventsMax=nEventsMax, color = r.kBlue)
            + supy.samples.specify(names="P3", nEventsMax=nEventsMax, color = r.kCyan)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1.0e-3) # /pb
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     samplesForRatios = ('SM', ['A2', 'A4', 'A6', 'P3']),
                     sampleLabelsForRatios = ('SM','BSM'),
                     ).plotAll()
