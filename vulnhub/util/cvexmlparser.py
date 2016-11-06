import xmltodict


def cvexmlparser(xmlfile):
    xmldoc = open(xmlfile, 'r')
    xmlcont = xmldoc.read()
    xmldoc.close()
    tree = xmltodict.parse(xmlcont)
    cve_entries = []

    for cve_item in tree['nvd'].get('entry'):

        cve_entry = dict()
        cve_entry['cve_id'] = cve_item['@id']

        cpes_entry = []
        if cve_item.get('vuln:vulnerable-software-list') and cve_item['vuln:vulnerable-software-list'].get('vuln:product'):
            if type(cve_item['vuln:vulnerable-software-list']['vuln:product']) == str:
                cpes_entry.append(cve_item['vuln:vulnerable-software-list']['vuln:product'])
            else:
                cpes_entry = list(cve_item['vuln:vulnerable-software-list']['vuln:product'])
            if not cpes_entry:
                cpes_entry.append('NO CPE Entry')
                print("hello")

        cve_entry['software_list'] = cpes_entry

        if cve_entry.get('vuln:published-datetime'):
            cve_entry['published_date'] = cve_item['vuln:published-datetime']
        else:
            pass
        cve_entry['modified_date'] = cve_item['vuln:last-modified-datetime']

        if cve_item.get('vuln:cvss') and cve_item['vuln:cvss'].get('cvss:base_metrics'):
            cve_entry['Base_Score'] = float(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:score'])
            # CVSS Base Information

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-vector']) != str:
                cve_entry['Base_Access_Vector'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-vector']['#text']
            else:
                cve_entry['Base_Access_Vector'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-vector']

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-complexity']) != str:
                cve_entry['Base_Access_Complexity'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-complexity']['#text']
            else:
                cve_entry['Base_Access_Complexity'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:access-complexity']

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:authentication']) != str:
                cve_entry['Base_Authentication'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:authentication']['#text']
            else:
                cve_entry['Base_Authentication'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:authentication']

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:confidentiality-impact']) != str:
                cve_entry['Base_Confidentiality_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:confidentiality-impact']['#text']
            else:
                cve_entry['Base_Confidentiality_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:confidentiality-impact']

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:integrity-impact'])!=str:
                cve_entry['Base_Integrity_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:integrity-impact']['#text']
            else:
                cve_entry['Base_Integrity_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:integrity-impact']

            if type(cve_item['vuln:cvss']['cvss:base_metrics']['cvss:availability-impact']) != str:
                cve_entry['Base_Availability_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:availability-impact']['#text']
            else:
                cve_entry['Base_Availability_Impact'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:availability-impact']
                
            cve_entry['Base_Source'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:source']
            cve_entry['Base_generation'] = cve_item['vuln:cvss']['cvss:base_metrics']['cvss:generated-on-datetime']

        cwe = []
        try:

            cwe.append(cve_item['vuln:cwe']['@id'])

        except KeyError:
            pass
        except TypeError:
            for cwe_entry in cve_item['vuln:cwe']:
                cwe.append(cwe_entry['@id'])

        cve_entry['cwe_id'] = list(cwe)

        # Fill from references dict

        if cve_item.get('vuln:references'):
            try:
                cve_entry['vulnerability_source'] = cve_item['vuln:references'][0]['vuln:source']
                vuln_source = ''
                if type(cve_entry['vulnerability_source_reference']) != str:
                    vuln_source = cve_entry['vulnerability_source_reference']['#text']
                else:
                    vuln_source = cve_item['vuln:references'][0]['vuln:reference']
                cve_entry['vulnerability_source_reference'] = vuln_source

            except KeyError:
                cve_entry['vulnerability_source'] = ''
                cve_entry['vulnerability_source_reference'] = ''
        else:
            cve_entry['vulnerability_source'] = ''
            cve_entry['vulnerability_source_reference'] = ''

        if cve_item.get('vuln:summary'):
            cve_entry['summary'] = cve_item['vuln:summary']

        # Add dictinoary to CVES list
        cve_entries.append(cve_entry)

    # Return list of dictionaries
    return cve_entries


if __name__ =='__main__':

    cvexmlparser('nvdcve-2.0-recent.xml')
