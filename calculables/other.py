import supy

class Indices(supy.wrappedChain.calculable) :
    """
    This is a calculable to build the collection of jets that have
    some pt min and eta max. It can be used also for other
    collections, as long as they have a pt and eta.
    """
    def __init__(self, collection = None):
        self.fixes = collection
        self.stash(['px','py','pz','ene'])
    @property
    def name(self) : return 'Indices%s%s' % self.fixes
    def update(self, _) :
        # Note to self: could also use 'n_leptons', 'n_jets' to
        # determine the numnber of elements, but then I would have
        # another parameter (the leaf name n_*) to specify. Use the px
        # vector size instead.
        pxs = self.source[self.px]
        self.value = [i for i in range(pxs.size())]
