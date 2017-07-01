from sections import * 

class Message(object):

    def __init__(self, data, offset):
        if len(data) < 16:
            return

        self.sections = []

        # Read Indication section
        indicatorSection = IndicatorSection(data[offset:])
        if not indicatorSection.valid:
            return
        self.sections.append(indicatorSection)
        self._data = data[offset:offset+self.sections[0].total_length]

        # Read Identification section
        offset = self.sections[-1].length
        self.sections.append(IdentificationSection(self._data, offset))

        # Read optional local use section
        offset += self.sections[-1].length
        local_use_section = LocalUseSection(self._data, offset)
        if local_use_section.exists:
            self.sections.append(local_use_section)
            offset += self.sections[-1].length

        # Read Grid Definition section
        self.sections.append(GridDefinitionSection(self._data, offset))

        # Read Product Definition section
        offset += self.sections[-1].length
        self.sections.append(ProductDefinitionSection(self._data, offset, self.sections[0].discipline_value))

        # Read Data Representation section
        offset += self.sections[-1].length
        self.sections.append(DataRepresentationSection(self._data, offset))

        # Read Bit Map section
        offset += self.sections[-1].length
        self.sections.append(BitMapSection(self._data, offset))

        # Read Data section
        offset += self.sections[-1].length
        self.sections.append(DataSection(self._data, offset, self.sections[4].template))

        # Read End section
        offset += self.sections[-1].length
        self.sections.append(EndSection(self._data, offset))

    @property
    def length(self):
        if len(self.sections) > 0:
            return self.sections[0].total_length
        else:
            return 0

    @property
    def section_count(self):
        return len(self.sections)

    def section_id(self, id):
        for sec in self.sections:
            if sec.section_number == id:
                return sec
        return None

def read_messages_raw(all_data, count=-1):
    messages = []

    offset = 0
    while offset < len(all_data):
        messages.append(Message(all_data, offset))
        offset = offset + messages[-1].length

        if count > 0 and len(messages) == count:
            break

    return messages

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
