from identified import *
from config import *
import rdflib
import os


class Document(Identified):
    """
    The Document is a container for all SBOL data objects.

    In a previous era, engineers might sit at a drafting board and draft a design by hand.
    The engineer's drafting sheet in LibSBOL is called a Document. The Document serves as a container,
    initially empty, for SBOL data objects. All file I/O operations are performed on the Document
    to populate it with SBOL objects representing design elements.
    """

    def __init__(self, filename=None):
        """
        Construct a document.

        :param filename: (optional) a file to initialize the Document.
        """
        super().__init__(SBOL_DOCUMENT, "", VERSION_STRING)
        # The Document's register of objects
        self.object_cache = {} # Needed?
        self.sbol_objects = None # Needed?
        self.resource_namespaces = None
        self.designs = Property(self, SYSBIO_DESIGN, '0', '*', [libsbol_rule_11])
        self.builds = Property(self, SYSBIO_BUILD, '0', '*', [libsbol_rule_12])
        self.tests = Property(self, SYSBIO_TEST, '0', '*', [libsbol_rule_13])
        self.analyses = Property(self, SYSBIO_ANALYSIS, '0', '*', [libsbol_rule_14])
        self.componentDefinitions = Property(self, SBOL_COMPONENT_DEFINITION, '0', '*', None)
        self.moduleDefinitions = Property(self, SBOL_MODULE_DEFINITION, '0', '*', None)
        self.models = Property(self, SBOL_MODEL, '0', '*', None)
        self.sequences = Property(self, SBOL_SEQUENCE, '0', '*', None)
        self.collections = Property(self, SBOL_COLLECTION, '0', '*', None)
        self.activities = Property(self, PROVO_ACTIVITY, '0', '*', None)
        self.plans = Property(self, PROVO_PLAN, '0', '*', None)
        self.agents = Property(self, PROVO_AGENT, '0', '*', None)
        self.attachments = Property(self, SBOL_ATTACHMENT, '0', '*', None)
        self.combinatorialderivations = Property(self, SBOL_COMBINATORIAL_DERIVATION, '0', '*', None)
        self.implementations = Property(self, SBOL_IMPLEMENTATION, '0', '*', None)
        self.sampleRosters = Property(self, SYSBIO_SAMPLE_ROSTER, '0', '*', [validation.libsbol_rule_16])
        self.experiments = Property(self, SBOL_EXPERIMENT, '0', '*', None)
        self.experimentalData = Property(self, SBOL_EXPERIMENTAL_DATA, '0', '*', None)
        self.citations = Property(self, PURL_URI + "bibliographicCitation", '0', '*', None)
        self.graph = None
        self.keywords = Property(self, PURL_URI + "elements/1.1/subject", '0', '*', None)

    def add(self, sbol_objs):
        """
        Register an object in the Document.

        :param sbol_objs: The SBOL object(s) you want to serialize. Either a single object or a list of objects.
        :return: None
        """
        for obj in sbol_objs:
            self.object_cache[obj.identity] = obj

    def addNamespace(self, ns, prefix):
        """Add a new namespace to the Document.

        :param ns: The namespace, eg. http://sbols.org/v2#
        :param prefix: The namespace prefix, eg. sbol
        :return:
        """
        raise NotImplementedError("Not yet implemented")

    def addComponentDefinition(self, sbol_obj):
        """
        Convenience method for adding a component definition.

        :param sbol_obj: component definition
        :return: None
        """
        self.componentDefinitions[sbol_obj.identity] = sbol_obj

    def addModuleDefinition(self, sbol_obj):
        """
        Convenience method for adding a module definition.

        :param sbol_obj: module definition
        :return: None
        """
        self.moduleDefinitions[sbol_obj.identity] = sbol_obj

    def addSequence(self, sbol_obj):
        """
        Convenience method for adding a sequence.

        :param sbol_obj: sequence
        :return: None
        """
        self.add([sbol_obj])

    def addModel(self, sbol_obj):
        """
        Convenience method for adding a model.

        :param sbol_obj: model
        :return: None
        """
        self.add([sbol_obj])

    def create(self, uri):
        """
        Creates another SBOL object derived from TopLevel and adds it to the Document.
        NOTE: originally from ReferencedObject
        :param uri: In "open world" mode, this is a full URI and the same as the returned URI.
        If the default namespace for libSBOL has been configured, then this argument should simply be a
        local identifier. If SBOL-compliance is enabled, this argument should be the intended
        displayId of the new object. A full URI is automatically generated and returned.
        :return: The full URI of the created object
        """
        if Config.getOption(ConfigOptions.SBOL_COMPLIANT_URIS.value) is True:
            obj = Identified()
            #obj.identity = os.path.join(getHomespace(), )
        raise NotImplementedError("Not yet implemented")


    def get(self, uri):
        """
        Retrieve an object from the Document.
cas9 = ComponentDefinition('Cas9', BIOPAX_PROTEIN)
        :param uri: The identity of the SBOL object you want to retrieve.
        :return: The SBOL object.
        """
        # TODO may want to move into SBOLObject or Property
        # First, search the object's property store for the uri
        if uri in self.object_cache:
            return self.object_cache[uri]
        if Config.getOption(ConfigOptions.SBOL_COMPLIANT_URIS) is True:
            return

    def getAll(self):
        """
        Retrieve a list of objects from the Document.

        :return: A list of objects from the Document.
        """
        raise NotImplementedError("Not yet implemented")

    def getComponentDefinition(self, uri):
        raise NotImplementedError("Not yet implemented")

    def getModuleDefinition(self, uri):
        raise NotImplementedError("Not yet implemented")

    def getSequence(self, uri):
        raise NotImplementedError("Not yet implemented")

    def getModel(self, uri):
        raise NotImplementedError("Not yet implemented")

    # File I/O #
    def write(self, filename):
        """
        Serialize all objects in this Document to an RDF/XML file.

        :param filename: The full name of the file you want to write (including file extension).
        :return: A string with the validation results, or empty string if validation is disabled.
        """
        raise NotImplementedError("Not yet implemented")

    def read(self, filename):
        """
        Read an RDF/XML file and attach the SBOL objects to this Document.

        Existing contents of the Document will be wiped.
        :param filename: The full name of the file you want to read (including file extension).
        :return: None
        """
        with open(filename, 'r') as f:
            graph = rdflib.Graph()
            graph.parse(f, format="application/rdf+xml")
            # top_query = "PREFIX : <http://example.org/ns#> " \
            #     "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> " \
            #     "PREFIX sbol: <http://sbols.org/v2#> " \
            #     "SELECT ?s ?o " \
            #     "{ ?s a ?o }"
            # top_level_results = graph.query(top_query)


    def readString(self, sbol_str):
        """
        Convert text in SBOL into data objects.

        :param sbol_str: A string formatted in SBOL.
        :return: None
        """
        raise NotImplementedError("Not yet implemented")

    def writeString(self):
        """
        Convert data objects in this Document into textual SBOL.

        :return: A string representation of the objects in this Document.
        """
        raise NotImplementedError("Not yet implemented")

    def append(self, filename):
        """
        Read an RDF/XML file and attach the SBOL objects to this Document.

        New objects will be added to the existing contents of the Document.
        :param filename: The full name of the file you want to read (including file extension).
        :return: None
        """
        raise NotImplementedError("Not yet implemented")

    # Online validation #
    def request_validation(self, sbol_str):
        # TODO what is this method supposed to do?
        raise NotImplementedError("Not yet implemented")

    def request_comparison(self, diff_file):
        """
        Perform comparison on Documents using the online validation tool.

        This is for cross-validation of SBOL documents with libSBOLj. Document comparison can also be performed
        using the built-in compare method.
        :param diff_file:
        :return: The comparison results
        """
        raise NotImplementedError("Not yet implemented")

    def clear(self):
        """
        Delete all properties and objects in the Document.

        :return: None
        """
        raise NotImplementedError("Not yet implemented")

    def query_repository(self, command):
        """

        :param command:
        :return: str
        """
        # TODO better docstring
        raise NotImplementedError("Not yet implemented")

    def search_metadata(self, role, type, name, collection):
        """

        :param role:
        :param type:
        :param name:
        :param collection:
        :return: str
        """
        # TODO better docstring
        raise NotImplementedError("Not yet implemented")

    # TODO The commented-out methods below are important, but they rely heavily on raptor
    # static std::string string_from_raptor_term(raptor_term *term, bool addWrapper=false);
    #
    # /// Generates rdf/xml
    # void generate(raptor_world** world, raptor_serializer** sbol_serializer, char** sbol_buffer, size_t* sbol_buffer_len, raptor_iostream** ios, raptor_uri** base_uri);

    def serialize_rdfxml(self, out):
        """
        Serialize RDF XML.
        :param out: output stream
        :return: None
        """
        raise NotImplementedError("Not yet implemented")

    def validate(self):
        """
        Run validation on this Document via the online validation tool.

        :return: A string containing a message with the validation results
        """
        raise NotImplementedError("Not yet implemented")

    def size(self):
        """
        Get the total number of objects in the Document, including SBOL core object and custom annotation objects.

        :return: The total number of objects in the Document.
        """
        raise NotImplementedError("Not yet implemented")

    def __len__(self):
        """
        Get the total number of objects in the Document, including SBOL core object and custom annotation objects.

        (Returns the same thing as size())

        :return: The total number of objects in the Document.
        """
        return self.size()

    def __str__(self):
        """
        Produce a string representation of the Document.

        :return: A string representation of the Document.
        """
        return self.summary()

    def __eq__(self, other):
        raise NotImplementedError("Not yet implemented")
        # if self.graph is None:
        #     return other.graph is None
        # else:
        #     return rdflib.compare.isomorphic(self.graph, other.graph)

    def cacheObjectsDocument(self):
        # TODO docstring
        raise NotImplementedError("Not yet implemented")

    def referenceNamespace(self, uri):
        """

        :param uri:
        :return: str
        """
        # TODO better docstring
        raise NotImplementedError("Not yet implemented")

    def summary(self):
        """
        Produce a string representation of the Document.

        :return: A string representation of the Document.
        """
        raise NotImplementedError("Not yet implemented")

    # TODO Port iterator, which loops over top-level items of Document

    def find(self, uri):
        """
        Search recursively for an SBOLObject in this Document that matches the uri.

        :param uri: The identity of the object to search for.
        :return: A pointer to the SBOLObject, or NULL if an object with this identity doesn't exist.
        """
        raise NotImplementedError("Not yet implemented")

    def getTypeURI(self):
        return SBOL_DOCUMENT
