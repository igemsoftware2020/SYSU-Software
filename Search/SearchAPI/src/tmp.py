def addElementHandler_(cnx, data) -> (bool, tuple):
    cursor = cnx.cursor()

    comdef_values = None
    seq_value_list = []
    com_value_list = []
    seqant_value_list = []
    location_value_list = []

    flag, message, comdef_values = comdefHandler(cursor, data)
    if flag == False:
        return False, message

    table = "Sequence"
    if table in data:
        for seqdata in data[table]:
            flag, message, seq_values = seqHandler(
                cursor, seqdata, comdef_values)
            if flag == False:
                return False, message
            seq_values["ownedBy"] = comdef_values["ownedBy"]
            seq_value_list.append(seq_values)

    table = "Component"
    if table in data:
        for comdata in data[table]:
            flag, message, com_values = comHandler(
                cursor, comdata, comdef_values)
            if flag == False:
                return False, message
            com_value_list.append(com_values)

    table = "SequenceAnnotation"
    if table in data:
        for seqantdata in data[table]:
            flag, message, seqant_values = seqantHandler(
                cursor, seqantdata, comdef_values)
            if flag == False:
                return False, message
            seqant_value_list.append(seqant_values)

            if "Location" not in seqantdata:
                return False, "At lease one location is needed for each SequenceAnnotation"

            for location_data in seqantdata["Location"]:
                flag, message, location_values = locationHandler(
                    cursor, location_data, seqant_values, comdef_values)
                if flag == False:
                    return False, message
                location_value_list.append(location_values)

    # insertData(cursor, comdef_values, "ComponentDefinition")

    # for seq_values in seq_value_list:
    #     insertData(cursor, seq_values, "Sequence")
    # for com_values in com_value_list:
    #     insertData(cursor, com_values, "Component")
    # for seqant_values in seqant_value_list:
    #     insertData(cursor, seqant_values, "SequenceAnnotation")
    # for location_values in location_value_list:
    #     insertData(cursor, location_values, "Location")

    insertHandler(cursor, comdef_values, "ComponentDefinition", is_list=False)
    insertHandler(cursor, seq_value_list, "Sequence", is_list=True)
    insertHandler(cursor, com_value_list, "Component", is_list=True)
    insertHandler(cursor, seqant_value_list,
                  "SequenceAnnotation", is_list=True)
    insertHandler(cursor, location_value_list, "Location", is_list=True)

    cnx.commit()
    cursor.close()

    return True, (comdef_values["displayId"], comdef_values["role"],)
