from . import sections

class Message(object):

    INDICATOR_SECTION_INDEX = 0
    IDENTIFICATION_SECTION_INDEX = 1
    GRID_DEFINITION_SECTION_INDEX = 2
    PRODUCT_DEFINITION_SECTION_INDEX = 3
    DATA_REPRESENTATION_SECTION_INDEX = 4
    BITMAP_SECTION_INDEX = 5
    DATA_SECTION_INDEX = 6
    END_SECTION_INDEX = 7

    def __init__(self, data, offset):
        if len(data) < 16:
            return

        self.sections = []

        # Read Indication section
        indicatorSection = sections.IndicatorSection(data[offset:])
        if not indicatorSection.valid:
            return
        self.sections.append(indicatorSection)
        self._data = data[offset:offset+self.sections[0].total_length]

        # Read Identification section
        offset = self.sections[-1].length
        self.sections.append(sections.IdentificationSection(self._data, offset))

        # Read optional local use section
        offset += self.sections[-1].length
        local_use_section = sections.LocalUseSection(self._data, offset)
        if local_use_section.exists:
            self.sections.append(local_use_section)
            offset += self.sections[-1].length

        # Read Grid Definition section
        self.sections.append(sections.GridDefinitionSection(self._data, offset))

        # Read Product Definition section
        offset += self.sections[-1].length
        self.sections.append(sections.ProductDefinitionSection(self._data, offset, self.sections[0].discipline_value))

        # Read Data Representation section
        offset += self.sections[-1].length
        self.sections.append(sections.DataRepresentationSection(self._data, offset))

        # Read Bit Map section
        offset += self.sections[-1].length
        self.sections.append(sections.BitMapSection(self._data, offset))

        # Read Data section
        offset += self.sections[-1].length
        self.sections.append(sections.DataSection(self._data, offset, self.sections[4].template))

        # Read End section
        offset += self.sections[-1].length
        self.sections.append(sections.EndSection(self._data, offset))

    @property
    def length(self):
        if len(self.sections) > 0:
            return self.sections[0].total_length
        else:
            return 0

    @property
    def section_count(self):
        return len(self.sections)

    @property
    def valid(self):
        if self.section_count < 7:
            return False
        return self.sections[-1].valid

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
