database_config = {
    'user': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'roadmapDB',
    'raise_on_warnings': True
}

role_char = {
    "CDS": "A",
    "RBS": "T",
    "Promoter": "R",
    "Terminator": "_",
    "Composite": "E"
}

insert_statements = {
    "ComponentDefinition": """
    insert into ComponentDefinition(
        persistentIdentity,
        displayId,
        version,
        wasDerivedFrom,
        wasGeneratedBy,
        title,
        description,
        created,
        modified,
        mutableProvenance,
        topLevel,
        mutableDescription,
        mutableNotes,
        creator,
        type,
        role,
        comRoleSeq,
        comRoleSeqRecursive,
        roleSeq,
        originRole,
        useRole,
        outputRole
        ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    "Sequence": "insert into Sequence values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "Component": "insert into Component values(%s, %s, %s, %s, %s, %s, %s, %s)",
    "SequenceAnnotation": "insert into SequenceAnnotation values(%s, %s, %s,%s, %s, %s, %s)",
    "Location": "insert into Location values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "DesignGraph": "insert into DesignGraph(persistentIdentity, article, description) values (%s, %s, %s)",
    "Activity": "insert into Activity values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "DesignGraph_ComponentDefinition": "insert into DesignGraph_ComponentDefinition values (%s, %s)",
    "DesignGraph_Activity": "insert into DesignGraph_Activity values (%s, %s)"
}

table_attrs = {
    "DesignGraph": [
        "persistentIdentity",
        "article",
        "description"
    ],
    "Activity": [
        "persistentIdentity",
        "displayId",
        "version",
        "title",
        "description",
        "topLevel",
        "ownedBy",
        "creator",
        "endedAtTime"
    ],
    "DesignGraph_ComponentDefinition": [
        "graph_id",
        "componentDefinition_id"
    ],
    "DesignGraph_Activity": [
        "designGraph_id",
        "activity_id"
    ],
    "ComponentDefinition": [
        "persistentIdentity",
        "displayId",
        "version",
        "wasDerivedFrom",
        "wasGeneratedBy",
        "title",
        "description",
        "created",
        "modified",
        "mutableProvenance",
        "topLevel",
        "mutableDescription",
        "mutableNotes",
        "creator",
        "type",
        "role",
        "comRoleSeq",
        "comRoleSeqRecursive",
        "roleSeq",
        "originRole",
        "useRole",
        "outputRole"
    ],
    "Sequence": [
        "persistentIdentity",
        "displayId",
        "version",
        "wasDerivedFrom",
        "wasGeneratedBy",
        "topLevel",
        "ownedBy",
        "elements",
        "encoding",
        "father_id"
    ],
    "Component": [
        "persistentIdentity",
        "displayId",
        "version",
        "title",
        "topLevel",
        "definition",
        "access",
        "father_id"
    ],
    "SequenceAnnotation": [
        "persistentIdentity",
        "displayId",
        "version",
        "title",
        "topLevel",
        "component",
        "father_id"
    ],
    "Location": [
        "persistentIdentity",
        "displayId",
        "version",
        "topLevel",
        "direction",
        "start",
        "end",
        "orientation",
        "father_id"
    ]
}

graph_handler_attr = [
    {
        "name": "article",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "description",
        "must": False,
        "unique": False,
        "in_database": False
    }
]

act_handler_attr = [
    {
        "name": "displayId",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "title",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "description",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "ownedBy",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "creator",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "endedAtTime",
        "must": False,
        "unique": False,
        "in_database": False
    }
]

comdef_handler_attr = [
    {
        "name": "displayId",
        "must": True,
        "unique": True,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "wasDerivedFrom",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "wasGeneratedBy",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "title",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "description",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "created",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "modified",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "mutableProvenance",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "mutableDescription",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "mutableNotes",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "creator",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "type",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "role",
        "must": True,
        "unique": False,
        "in_database": False
    }
]

seq_handler_attr = [
    {
        "name": "displayId",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "wasDerivedFrom",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "wasGeneratedBy",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "ownedBy",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "elements",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "encoding",
        "must": False,
        "unique": False,
        "in_database": False
    }
]

com_handler_attr = [
    {
        "name": "displayId",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "title",
        "must": True,
        "unique": True,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "definition",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "access",
        "must": False,
        "unique": False,
        "in_database": False
    }
]

seqant_handler_attr = [
    {
        "name": "displayId",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "title",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    }
]

location_handler_attr = [
    {
        "name": "displayId",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "version",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "topLevel",
        "must": False,
        "unique": False,
        "in_database": False
    },
    {
        "name": "direction",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "start",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "end",
        "must": True,
        "unique": False,
        "in_database": False
    },
    {
        "name": "orientation",
        "must": False,
        "unique": False,
        "in_database": False
    }
]
