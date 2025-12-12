import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring

def generate_define_xml(df):
    root = Element('DefineXML')
    study = SubElement(root, 'Study')
    study.set('OID', 'SP.1')
    metadata = SubElement(study, 'MetaDataVersion')
    metadata.set('Name', 'ZeroEDC Auto-Generated')
    return tostring(root, encoding='unicode')

if __name__ == "__main__":
    print(generate_define_xml(pd.DataFrame()))
