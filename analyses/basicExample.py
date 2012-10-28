import calculables, supy, ROOT as r

class basicExample(supy.analysis) :

    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.value('n_jets',20, 0, 20),
            supy.steps.histos.value('top_ene',20,0,1e4),
            #supy.steps.histos.energy("top_P4", 20,0,1e4), # just to verify that P4 is consistent with ntuple
            supy.steps.histos.pt("top_P4", 100,1,201),
            supy.steps.histos.pt("jet_P4", 100,1,201, indices = 'Indicesjet_'),
            supy.steps.histos.eta("top_P4", 100,-10,10),
            supy.steps.histos.eta("antitop_P4", 100,-10,10),
            supy.steps.histos.absEta("top_P4", 100,10,10),
            supy.steps.histos.absEta("antitop_P4", 100,10,10),
            supy.steps.histos.pt('TtbarP4', 50,0,+0.05e-4),
            supy.steps.histos.mass('TtbarP4', 100,0,2e3),
            supy.steps.histos.value('AbsSumRapidities', 100,0,10),
            ]


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
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ]
                 +[calculables.other.Indices(collection=("jet_",""))]
                 +[calculables.kinematic.P4(collection = ("jet_",""))]
                 +[calculables.kinematic.singleP4(collection = ("top_",""))]
                 +[calculables.kinematic.singleP4(collection = ("antitop_",""))]
                 +[calculables.kinematic.TtbarP4(), calculables.kinematic.AbsSumRapidities()]
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
        test = True
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
