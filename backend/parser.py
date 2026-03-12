import xml.etree.ElementTree as ET
from datetime import datetime
from database import SessionLocal, CPEMessage, init_db
import os

NS = {
    'cpe': 'http://cpe.mitre.org/dictionary/2.0',
    'cpe-23': 'http://scap.nist.gov/schema/cpe-extension/2.3'
}

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
    except Exception:
        return None

def parse_xml_and_store(file_path):
    print(f"Starting to parse {file_path}...")
    init_db()
    db = SessionLocal()
    
    context = ET.iterparse(file_path, events=('end',))
    count = 0
    cpes_batch = []
    
    for event, elem in context:
        if elem.tag == '{' + NS['cpe'] + '}cpe-item':
            cpe_22_uri = elem.get('name')
            cpe_22_deprecated_date = parse_date(elem.get('deprecation_date'))
            
            title_elem = elem.find('cpe:title', NS)
            cpe_title = title_elem.text if title_elem is not None else "No Title"
            
            refs = []
            refs_elem = elem.find('cpe:references', NS)
            if refs_elem is not None:
                for ref in refs_elem.findall('cpe:reference', NS):
                    href = ref.get('href')
                    if href:
                        refs.append(href)
            
            cpe_23_elem = elem.find('cpe-23:cpe23-item', NS)
            cpe_23_uri = None
            cpe_23_deprecated_date = None
            if cpe_23_elem is not None:
                cpe_23_uri = cpe_23_elem.get('name')
                cpe_23_deprecated_date = parse_date(cpe_23_elem.get('deprecation_date'))
            
            cpe_entry = CPEMessage(
                cpe_title=cpe_title,
                cpe_22_uri=cpe_22_uri,
                cpe_23_uri=cpe_23_uri,
                reference_links=refs,
                cpe_22_deprecation_date=cpe_22_deprecated_date,
                cpe_23_deprecation_date=cpe_23_deprecated_date
            )
            cpes_batch.append(cpe_entry)
            
            if count >= 10000:
                print("Limit reached, stopping parser.")
                break
            
            if len(cpes_batch) >= 1000:
                db.bulk_save_objects(cpes_batch)
                db.commit()
                cpes_batch = []
                count += 1000
                print(f"Processed {count} entries...")
            
            elem.clear()
            
    if cpes_batch:
        db.bulk_save_objects(cpes_batch)
        db.commit()
        count += len(cpes_batch)
    
    print(f"Finished parsing. Total entries: {count}")
    db.close()

if __name__ == "__main__":
    xml_path = r"d:\securin\official-cpe-dictionary_v2.xml"
    if os.path.exists(xml_path):
        parse_xml_and_store(xml_path)
    else:
        print(f"File not found: {xml_path}")
