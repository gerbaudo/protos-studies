import supy, ROOT as r

class basicExample(supy.analysis) :

    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.value('n_jets',20, 0, 20),
            supy.steps.histos.value('top_ene',20,0,1e4),
            ]

    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ]
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
