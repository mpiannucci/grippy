from sections import IndicatorSection, IdentificationSection

class Message(object):

    def __init__(self, data, offset):
        if len(data) < 16:
            return

        self.sections = []

        # Read first section
        self.sections.append(IndicatorSection(data[offset:]))
        self._data = data[offset:offset+self.sections[-1].total_length]

        # Read second section
        self.sections.append(IdentificationSection(self._data, self.sections[-1].length))

    @property
    def length(self):
        if len(self.sections) > 0:
            return self.sections[0].total_length
        else:
            return 0

    @property
    def section_count(self):
        return len(self.sections)

def read_messages(filename, count=-1):
    messages = []
    with open(filename, 'rb') as stream:
        all_data = stream.read()
 
    offset = 0
    while offset < len(all_data):
        messages.append(Message(all_data, offset))
        offset = offset + messages[-1].length

        if count > 0 and len(messages) == count:
            break

    return messages
