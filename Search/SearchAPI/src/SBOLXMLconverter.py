# coding=utf-8
import xml.dom.minidom
import json
import sys
import os


# Waring This is only for macOS or Unix(Linux) Operating System
# , __source_SBOLxml_addr__, __converted_json_addr__):
def SBOLxml_to_json(data):
    # basic_address = 'https://synbiohub.org/public/igem/'

    # __source_SBOLxml_addr__  =  '/Users/mac/Downloads/BBa_B3202.xml'
    # You need to implement the output address here
    # __converted_json_addr__  = '/Users/mac/Downloads/test.json'
    # os.open(__converted_json_addr__,os.O_RDWR)

    # 打开xml文档
    # dom = xml.dom.minidom.parse(__source_SBOLxml_addr__)
    dom = xml.dom.minidom.parseString(data)
    # 得到文档元素对象
    root = dom.documentElement

    # json: persistentIdentity
    # get persistentIdentity = filename, using /path/filename.format
    # file_name_spliter0 = __source_SBOLxml_addr__.split("/")
    # file_name_spliter = file_name_spliter0[-1].split(".")
    # persistentIdentity = file_name_spliter[-1]

    # json: article
    # Assume article is in XML arrtibute: [rdf:resource]
    # find_article = root.getElementsByTagName('article')
    # article = None
    # else:
    # article = find_article[0].getAttribute('rdf:resource')

    # json: description
    # find_description = root.getElementsByTagName('description')
    # description = None
    # else:
    # article = find_article[0].getAttribute('rdf:resource')

    # json: Activity found
    find_pA = root.getElementsByTagName('prov:Activity')

    Activities = list()
    if(len(find_pA) != 0):
        for pA in find_pA:
            Act = {}
            # Activity: persistentID
            find_spI = pA.getElementsByTagName('sbol:persistentIdentity')
            persistentIdentity1 = find_spI[0].getAttribute('rdf:resource')
            Act["persistentIdentity"] = persistentIdentity1
            # Activity: displayId
            find_dID = pA.getElementsByTagName('sbol:displayId')
            displayID1 = find_dID[0].firstChild.data
            Act["displayID"] = displayID1
            # Activity: version
            find_version = pA.getElementsByTagName('sbol:version')
            version1 = find_version[0].firstChild.data
            Act["version"] = version1
            # Activity: title
            find_title = pA.getElementsByTagName('dcterms:title')
            if not(find_title == [] or find_title is None):
                title1 = find_title[0].firstChild.data
                Act["title"] = title1
            # Activity: description
            find_description = pA.getElementsByTagName('dcterms:description')
            description1 = find_description[0].firstChild.data
            Act["description"] = description1
            # Activity: topLevel
            find_topLevel = pA.getElementsByTagName('sbh:topLevel')
            topLevel1 = find_topLevel[0].getAttribute('rdf:resource')
            Act["topLevel"] = topLevel1
            # Activity: ownedBy
            find_ownedBy = pA.getElementsByTagName('sbh:ownedBy')
            ownedBy = [0]*len(find_ownedBy)
            for i in range(len(find_ownedBy)):
                ownedBy[i] = find_ownedBy[i].getAttribute('rdf:resource')
            Act["ownedBy"] = ownedBy
            # Activity: creator
            find_creator = pA.getElementsByTagName('dc:creator')
            creator = [0]*len(find_creator)
            for i in range(len(find_creator)):
                creator[i] = find_creator[i].firstChild.data
            Act["creator"] = creator
            # Activity: endedAtTime
            find_endedAtTime = pA.getElementsByTagName('prov:endedAtTime')
            endedAtTime = find_endedAtTime[0].firstChild.data
            Act["endedAtTime"] = endedAtTime
            # Add them to dic
            Activities.append(Act)

    '''
    d = {"persistentIdentity":persistentIdentity,
    "article":article,
    "description":description,
    "Activity":[
        {
            "persistentIdentity":persistentIdentity1,
            "displayID":displayID1,
            "version":version1,
            "title":title1,
            "description":description1,
            "topLevel":topLevel1,
            "ownedBy":ownedBy,
            "creator":creator,
            "endedAtTime":endedAtTime,

        }]
    # "ComponentDefinition":,
    }
    '''
    find_ComponentDefinitions = root.getElementsByTagName(
        'sbol:ComponentDefinition')
    ComponentDefinitions = list()
    if(len(find_ComponentDefinitions) != 0):
        for cd in find_ComponentDefinitions:
            CompDefi = {}
            # Activity: persistentID
            # persistentIdentity2 = cd.getElementsByTagName('sbol:persistentIdentity')[0].getAttribute('rdf:resource')

            displayId2 = cd.getElementsByTagName('sbol:displayId')[
                0].firstChild.data
            CompDefi["displayId"] = displayId2
            version2 = cd.getElementsByTagName('sbol:version')[
                0].firstChild.data
            CompDefi["version"] = version2
            if(len(cd.getElementsByTagName('sbol:wasDerivedFrom')) != 0):
                wasDerivedFrom2 = cd.getElementsByTagName('sbol:wasDerivedFrom')[
                    0].getAttribute('rdf:resource')
                CompDefi["wasDerivedFrom"] = wasDerivedFrom2
            if(len(cd.getElementsByTagName('sbol:wasGeneratedBy')) != 0):
                wasGeneratedBy2 = cd.getElementsByTagName('sbol:wasGeneratedBy')[
                    0].getAttribute('rdf:resource')
                CompDefi["wasGeneratedBy"] = wasGeneratedBy2
            title2 = cd.getElementsByTagName('dcterms:title')[
                0].firstChild.data
            CompDefi["title"] = title2
            description2 = cd.getElementsByTagName('dcterms:description')[
                0].firstChild.data
            CompDefi["description"] = description2
            CompDefi["created"] = cd.getElementsByTagName('dcterms:created')[
                0].firstChild.data
            CompDefi["modified"] = cd.getElementsByTagName('dcterms:modified')[
                0].firstChild.data
            CompDefi["topLevel"] = cd.getElementsByTagName(
                'sbh:topLevel')[0].getAttribute('rdf:resource')

            find_ownedBy2 = cd.getElementsByTagName('sbh:ownedBy')
            ownedBy2 = [0]*len(find_ownedBy2)
            for i in range(len(find_ownedBy2)):
                ownedBy2[i] = find_ownedBy2[i].getAttribute('rdf:resource')
            CompDefi["ownedBy"] = ownedBy2

            CompDefi['mutableDescription'] = cd.getElementsByTagName(
                'sbh:mutableDescription')[0].firstChild.data
            if(len(cd.getElementsByTagName('sbh:mutableNotes')) != 0):
                CompDefi['mutableNotes'] = cd.getElementsByTagName('sbh:mutableNotes')[
                    0].firstChild.data
            # mutableProvenance2 = cd.getElementsByTagName('sbh:mutableProvenance')[0].firstChild.data

            find_creator2 = cd.getElementsByTagName('dc:creator')
            creator2 = [0]*len(find_creator2)
            for i in range(len(find_creator2)):
                creator2[i] = find_creator2[i].firstChild.data
            CompDefi["creator"] = creator2

            CompDefi['type'] = cd.getElementsByTagName(
                'sbol:type')[0].getAttribute('rdf:resource')
            # role
            find_role2 = cd.getElementsByTagName('sbol:role')
            for r in find_role2:
                tmp = r.getAttribute('rdf:resource').split("/")[-1]
                if tmp == 'cds' or tmp == 'rbs' or tmp == 'promoter' or tmp == 'terminator':
                    CompDefi["role"] = tmp
                else:
                    CompDefi["role"] = "Composite"
            # sequence
            find_sequence2 = root.getElementsByTagName('sbol:Sequence')
            if(len(find_sequence2) != 0):
                # find the corresponding sequence
                sequences = []
                sq_properties = {}
                target_seq = cd.getElementsByTagName('sbol:sequence')[
                    0].getAttribute('rdf:resource')
                for subseq in find_sequence2:
                    if(subseq.getAttribute('rdf:about') == target_seq):
                        sq_properties["wasGeneratedBy"] = subseq.getElementsByTagName(
                            "prov:wasGeneratedBy")[0].getAttribute("rdf:resource")
                        sq_properties["encoding"] = subseq.getElementsByTagName(
                            "sbol:encoding")[0].getAttribute("rdf:resource")
                        # IMPORTANT
                        sq_properties["elements"] = subseq.getElementsByTagName("sbol:elements")[
                            0].firstChild.data
                        sq_properties["displayId"] = subseq.getElementsByTagName("sbol:displayId")[
                            0].firstChild.data
                        sq_properties["version"] = subseq.getElementsByTagName("sbol:version")[
                            0].firstChild.data
                        sq_properties["topLevel"] = subseq.getElementsByTagName(
                            "sbh:topLevel")[0].getAttribute("rdf:resource")
                        sequences.append(sq_properties)
                        CompDefi["Sequence"] = sequences
                        break
            else:
                CompDefi["Sequence"] = None

            # sbol:component
            find_components = cd.getElementsByTagName('sbol:Component')
            Components = []
            if(len(find_components) != 0):
                for cps in find_components:
                    Component_properties = {}
                    Component_properties["displayId"] = cps.getElementsByTagName("sbol:displayId")[
                        0].firstChild.data
                    Component_properties["title"] = cps.getElementsByTagName("dcterms:title")[
                        0].firstChild.data
                    Component_properties["topLevel"] = cps.getElementsByTagName(
                        "sbh:topLevel")[0].getAttribute("rdf:resource")
                    Component_properties["definition"] = cps.getElementsByTagName(
                        "sbol:definition")[0].getAttribute("rdf:resource")
                    Components.append(Component_properties)
            CompDefi['Component'] = Components

            # SequenceAnnotation
            find_sequenceAnnotations = cd.getElementsByTagName(
                'sbol:sequenceAnnotation')
            sAnnotations = []
            if(len(find_components) != 0):
                for sAs in find_sequenceAnnotations:
                    sAnnotation_properties = {}
                    sAnnotation_properties["displayId"] = sAs.getElementsByTagName(
                        "sbol:SequenceAnnotation")[0].getElementsByTagName("sbol:displayId")[0].firstChild.data
                    sAnnotation_properties["title"] = sAs.getElementsByTagName(
                        "sbol:SequenceAnnotation")[0].getElementsByTagName("dcterms:title")[0].firstChild.data
                    sAnnotation_properties["topLevel"] = sAs.getElementsByTagName("sbol:SequenceAnnotation")[
                        0].getElementsByTagName("sbh:topLevel")[0].getAttribute("rdf:resource")
                    sAnnotation_properties["component"] = sAs.getElementsByTagName("sbol:SequenceAnnotation")[
                        0].getElementsByTagName("sbol:component")[0].getAttribute("rdf:resource")
                    location_properties = {}
                    Location = []
                    find_locs = sAs.getElementsByTagName('sbol:location')
                    for loc in find_locs:
                        r = loc.getElementsByTagName("sbol:Range")
                        displayId3 = r[0].getElementsByTagName(
                            'sbol:displayId')
                        location_properties["displayId"] = displayId3[0].firstChild.data
                        topLevel3 = r[0].getElementsByTagName('sbh:topLevel')
                        location_properties["topLevel"] = topLevel3[0].getAttribute(
                            'rdf:resource')
                        orientation3 = r[0].getElementsByTagName(
                            'sbol:orientation')
                        location_properties["orientation"] = orientation3[0].getAttribute(
                            'rdf:resource')
                        direction3 = r[0].getElementsByTagName(
                            'igem:direction')
                        location_properties["igem:direction"] = direction3[0].getAttribute(
                            'rdf:resource')
                        start3 = r[0].getElementsByTagName('sbol:start')
                        location_properties["start"] = start3[0].firstChild.data
                        end3 = r[0].getElementsByTagName('sbol:end')
                        location_properties["end"] = end3[0].firstChild.data
                        Location.append(location_properties)
                    sAnnotation_properties["location"] = Location
                    sAnnotations.append(sAnnotation_properties)
            CompDefi['SequenceAnnotation'] = sAnnotations
            ComponentDefinitions.append(CompDefi)

    d = {}
    d['Activity'] = Activities
    # d['article'] = article
    # d['description'] = description
    d['ComponentDefinition'] = ComponentDefinitions
    jsonOut = json.dumps(d, indent=4, separators=(',', ': '))
    # f = open("demofile2.json", "w")
    # f.write(jsonOut)
    # f.close()
    # print(jsonOut)
    return jsonOut


# Test
# __source_SBOLxml_addr__ = '/media/gwen/DATA/A_GW/Competitions/IGEM/SBOL-JSON-Converter/BBa_B3202.xml'
# # You need to implement the output address here
# __converted_json_addr__ = '/media/gwen/DATA/A_GW/Competitions/IGEM/SBOL-JSON-Converter/test.json'
# SBOLxml_to_json(__source_SBOLxml_addr__, __converted_json_addr__)
