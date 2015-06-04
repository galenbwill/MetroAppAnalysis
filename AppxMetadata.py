import xml.sax

class AppxMetadata ( xml.sax.ContentHandler ):

    CATEGORY_IN_PROCESS = 'windows.activatableClass.inProcessServer'
    CATEGORY_PROXY_STUB = 'windows.activatableClass.proxyStub'

    def __init__(self):
        self.CurrentData = ''
        self.CurrentCategory = ''

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

    def handleApplication(self, attributes):
        self.id = attributes.get('Id')
        self.executable = attributes.get('Executable')
        if self.executable == None:
            self.type = 'WinJS'
        else:
            self.type = 'Native'

    def handleCapability(self, attributes):
        self.capabilities.append(attributes.get('Name'))

    def handleDeviceCapability(self, attributes):
        self.deviceCapabilities.append(attributes.get('Name'))

    def handleIdentity(self, attributes):
        self.architecture = attributes.get('ProcessorArchitecture')

    def handleProtocol(self, attributes):
        self.protocols.append(attributes.get('Name'))

    def handleExtension(self, attributes):
        self.CurrentCategory = attributes.get('Category')

    def characters(self, content):
        if self.CurrentData == 'Path' and self.CurrentCategory == self.CATEGORY_IN_PROCESS:
            self.inProcessServers.append(content)
        if self.CurrentData == 'Path' and self.CurrentCategory == self.CATEGORY_PROXY_STUB:
            self.proxyStubs.append(content)
        if self.CurrentData == 'FileType':
            self.fileTypes.append(content)

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

    # Call when an elements ends
    def endElement(self, tag):
        pass

    def __str__(self):
        st =  'App: ' + self.id
        st += '\n\tType: ' + self.type
        if self.executable != None:
            st += '\n\tExecutable: ' + self.executable
        st += '\n\tArchitecture: ' + self.architecture

        st += '\n\tCapabilities: ' + ''.join(self.capabilities)
        st += '\n\tDevice Capabilities: ' + ''.join(self.deviceCapabilities)
        st += '\n\tProtocols: ' + ''.join(self.protocols)
        st += '\n\tIn Process Servers: ' + ''.join(self.inProcessServers)
        st += '\n\tProxy Stubs: ' + ''.join(self.proxyStubs)
        st += '\n\tFile Types: ' + ''.join(self.fileTypes)

        return st

if ( __name__ == "__main__"):

   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = AppxMetadata()
   parser.setContentHandler( Handler )

   parser.parse('Maps.xml')
   print(Handler)
