__author__ = 'charles'
import xml.sax

class AppxMetadataSaxHandler ( xml.sax.ContentHandler ):

    CATEGORY_IN_PROCESS = 'windows.activatableClass.inProcessServer'
    CATEGORY_PROXY_STUB = 'windows.activatableClass.proxyStub'

    def __init__(self, show_all=False):
        self.show_all = show_all
        self.CurrentData = ''
        self.CurrentCategory = ''

        self.name = ''
        self.capabilities = []
        self.deviceCapabilities = []
        self.type = ''
        self.architecture = ''
        self.id = ''
        self.executable = None
        self.protocols = []
        self.inProcessServers = []
        self.proxyStubs = []
        self.fileTypes = []
        self.framework = None
        self.tileUpdateURI = None
        self.tileUpdateFrequency = None

    def handleApplication(self, attributes):
        self.id = attributes.get('Id')
        self.executable = attributes.get('Executable')
        if self.executable is None:
            self.type = 'WinJS'
        else:
            self.type = 'Native'

    def handleCapability(self, attributes):
        self.capabilities.append(attributes.get('Name'))

    def handleDeviceCapability(self, attributes):
        self.deviceCapabilities.append(attributes.get('Name'))

    def handleIdentity(self, attributes):
        self.architecture = attributes.get('ProcessorArchitecture')
        self.name = attributes.get('Name')

    def handleProtocol(self, attributes):
        self.protocols.append(attributes.get('Name'))

    def handleExtension(self, attributes):
        self.CurrentCategory = attributes.get('Category')

    def handleTileUpdate(self, attributes):
        self.tileUpdateURI = attributes.get('UriTemplate')
        self.tileUpdateFrequency = attributes.get('Recurrence')

    def characters(self, content):
        if len(content.strip()):
            if self.CurrentData == 'Path' and self.CurrentCategory == self.CATEGORY_IN_PROCESS:
                self.inProcessServers.append(content)
            if self.CurrentData == 'Path' and self.CurrentCategory == self.CATEGORY_PROXY_STUB:
                self.proxyStubs.append(content)
            if self.CurrentData == 'FileType':
                self.fileTypes.append(content)
            if self.CurrentData == 'Framework':
                self.framework = content == 'true'

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'Application':
            self.handleApplication(attributes)
        elif tag == 'Capability':
            self.handleCapability(attributes)
        elif tag == 'DeviceCapability':
            self.handleDeviceCapability(attributes)
        elif tag == 'Identity':
            self.handleIdentity(attributes)
        elif tag == 'Protocol':
            self.handleProtocol(attributes)
        elif tag == 'Extension':
            self.handleExtension(attributes)
        elif tag == 'wb:TileUpdate':
            self.handleTileUpdate(attributes)
#         elif tag == 'Framework':
#             self.handleFramework(attributes)

    # Call when an elements ends
    def endElement(self, tag):
        pass

    def show_prop(self, prop, label, joiner=u', ', show_all=False):
        value = self.__dict__[prop]
        if show_all is False and value is None:
            return ''
        if isinstance(value, list):
            if show_all is False and len(value) == 0:
                return ''
            value = joiner.join(value)
        return '%s: %s' % (label, value)

    PROPS = [
        ('name', 'App'),
        'Type',
        'Executable',
        'Architecture',
        'Capabilities',
        ('deviceCapabilities', 'Device Capabilities'),
        'Protocols',
        ('inProcessServers', 'In Process Servers'),
        ('proxyStubs', 'Proxy Stubs'),
        ('fileTypes', 'File Types')
    ]

    def __str__(self):
        if self.framework is True:
            st = 'Framework: ' + self.name
        else:
            st = ''
            for name in self.PROPS:
                if isinstance(name, tuple):
                    prop = name[0]
                    name = name[1]
                else:
                    prop = name.lower()
                p = self.show_prop(prop, name)
                if len(p):
                    if len(st):
                        st += '\n\t'
                    st += p
        return st

class AppxMetadataParser:

    def __init__(self):
        # create an XMLReader
        self.parser = xml.sax.make_parser()
        # turn off namespaces
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.urls = []

    def parse(self, source, show_all=False):
        # override the default ContextHandler
        self.Handler = AppxMetadataSaxHandler(show_all=show_all)
        self.parser.setContentHandler( self.Handler )
        self.parser.parse(source)
        return self

    def __str__(self):
        return str(self.Handler)

if ( __name__ == "__main__"):

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = AppxMetadataSaxHandler()
    parser.setContentHandler( Handler )

    parser.parse('test/Maps.xml')
    print(Handler)
