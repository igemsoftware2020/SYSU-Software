USE roadmapDB;

SET SESSION SQL_MODE=ANSI_QUOTES;

-- TODO reorganization

-- BEGIN TRANSACTION;


------ iGEM registry ------


DROP TABLE IF EXISTS "DesignGraph_Activity";
DROP TABLE IF EXISTS "Location";
DROP TABLE IF EXISTS "SequenceAnnotation";
DROP TABLE IF EXISTS "Component";
DROP TABLE IF EXISTS "DesignGraph_ComponentDefinition";
DROP TABLE IF EXISTS "DesignGraph_ComponentDefinition2";
DROP TABLE IF EXISTS "Sequence";
DROP TABLE IF EXISTS "ComponentDefinition"; 
DROP TABLE IF EXISTS "DesignGraph";
DROP TABLE IF EXISTS "Activity";


CREATE TABLE IF NOT EXISTS "Activity"(
    "persistentIdentity"    varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
    "title"                 varchar(200),
    "description"	        TEXT,
    "topLevel"              varchar(200),
    "ownedBy"               TEXT,
    "creator"               TEXT,
    "endedAtTime"           varchar(50),
    PRIMARY KEY("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "DesignGraph"(
    "persistentIdentity"    varchar(200) not null,
    "article"               TEXT,
    "description"           TEXT,
    "activity_id"           varchar(200),
    PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("activity_id") REFERENCES "Activity"("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "ComponentDefinition"(
    "persistentIdentity"	varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
	"wasDerivedFrom"	    TEXT,
	"wasGeneratedBy"    	TEXT,
    "title"                 varchar(200),
    "description"           TEXT,
    "created"               varchar(200),
    "modified"              varchar(200),
    "mutableProvenance"     TEXT,
    "topLevel"              varchar(200),
    "mutableDescription"    TEXT,
    "mutableNotes"          TEXT,
    "creator"               TEXT,
    "type"                  varchar(200),
    "role"                  TEXT,
    PRIMARY KEY("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "Sequence" (
	"persistentIdentity"	varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
	"wasDerivedFrom"	    TEXT,
	"wasGeneratedBy"    	TEXT,
    "topLevel"              varchar(200),
    "ownedBy"               TEXT,
    "elements"          	TEXT NOT NULL,
	"encoding"	            varchar(200),
    "father_id"             varchar(200),
	PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("father_id") REFERENCES "ComponentDefinition"("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "DesignGraph_ComponentDefinition"(
    "graph_id"               varchar(200),
    "componentDefinition_id" varchar(200),
    PRIMARY KEY("graph_id", "componentDefinition_id")
);

CREATE TABLE IF NOT EXISTS "Component" (
    "persistentIdentity"	varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
    "title"                 varchar(200),
    "topLevel"              varchar(200),
    "definition"            varchar(200),
    "access"                varchar(200),
    "father_id"             varchar(200),
	PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("father_id") REFERENCES "ComponentDefinition"("persistentIdentity")
);


CREATE TABLE IF NOT EXISTS "SequenceAnnotation" (
	"persistentIdentity"	varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
    "title"                 varchar(200),
    "topLevel"              varchar(200),
    "component"             varchar(200),
    "father_id"             varchar(200),
	PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("father_id") REFERENCES "ComponentDefinition"("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "Location" (
    "persistentIdentity"	varchar(200),
	"displayId"	            varchar(200),
	"version"	            varchar(50),
    "topLevel"              varchar(200),
    "direction"             varchar(200),
    "start"                 integer, -- included
    "end"                   integer, -- excluded
    "orientation"           varchar(200),
    "father_id"             varchar(200),
	PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("father_id") REFERENCES "SequenceAnnotation"("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "DesignGraph_Activity"(
    "designGraph_id"        varchar(200),
    "activity_id"           varchar(200),
    PRIMARY KEY("designGraph_id", "activity_id"),
    FOREIGN KEY("designGraph_id") REFERENCES "DesignGraph"("persistentIdentity"),
    FOREIGN KEY("activity_id") REFERENCES "Activity"("persistentIdentity")
);

----- Paper ----- 

DROP TABLE IF EXISTS "PaperComponentDefinition_PaperGraph";
DROP TABLE IF EXISTS "PaperGraph";
DROP TABLE IF EXISTS "PaperComponentDefinition";
DROP TABLE IF EXISTS "Paper";

CREATE TABLE IF NOT EXISTS "Paper"(
    "persistentIdentity"    integer not null AUTO_INCREMENT,
    "title"                 text,
    "url"                   varchar(400),
    "authors"               text,
    "abstract"              text,
    "year"                  integer,
    "vol"                   integer,
    "issue"                 integer,
    "type"                  varchar(50),
    "date"                  varchar(50),
    "jourName"              varchar(200),
    PRIMARY KEY("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "PaperGraph"(
    "persistentIdentity"    integer not null,
    "role_seq"              varchar(200),
    "father_id"             integer not null,
    PRIMARY KEY("persistentIdentity"),
    FOREIGN KEY("father_id") REFERENCES "Paper"("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "PaperComponentDefinition"(
    "persistentIdentity"    integer not null,
    "origin_name"           varchar(100),
    "origin_role"           varchar(50),
    "full_name"             varchar(100),
    "abbr_name"             varchar(100),
    "role"                  varchar(50),
    "role_seq"              varchar(10),
    PRIMARY KEY("persistentIdentity")
);

CREATE TABLE IF NOT EXISTS "PaperComponentDefinition_PaperGraph"(
    "graph_id"               integer not null,
    "componentDefinition_id" integer not null,
    "idx"                    integer,
    PRIMARY KEY ("graph_id", "componentDefinition_id", "idx"),
    FOREIGN KEY ("graph_id") REFERENCES "PaperGraph"("persistentIdentity"),
    FOREIGN KEY ("componentDefinition_id") REFERENCES "PaperComponentDefinition"("persistentIdentity")
);


----- UniprotCDS ----- 

DROP TABLE IF EXISTS "UniprotCDS";

CREATE TABLE IF NOT EXISTS "UniprotCDS"(
	"persistentIdentity"  integer not null auto_increment,
    "name"                varchar(200),
    "synonyms"            varchar(100),
    "ordered_locus_name"  varchar(100),
    "ORF_name"            varchar(100),
    "protein_name"        varchar(200),
    PRIMARY KEY ("persistentIdentity")
);

----- GenenetDB -----

DROP TABLE IF EXISTS "TF_ComponentDefinition";

CREATE TABLE IF NOT EXISTS "TF_ComponentDefinition"(
	"persistentIdentity"   integer not null auto_increment,
    "TF_name"              varchar(200),
    "gene_name"            varchar(200),
    PRIMARY KEY ("persistentIdentity")
);

CREATE INDEX "search_displayId" ON "ComponentDefinition" ("displayId");
CREATE INDEX "search_title" ON "ComponentDefinition" ("title");
CREATE INDEX "search_name" ON "ComponentDefinition" ("displayId", "title");
CREATE INDEX "search_CDS_0" ON "UniprotCDS" ("name");
CREATE INDEX "search_CDS_1" ON "UniprotCDS" ("synonyms");
CREATE INDEX "search_CDS_2" ON "UniprotCDS" ("ordered_locus_name");
CREATE INDEX "search_CDS_3" ON "UniprotCDS" ("ORF_name");
CREATE INDEX "search_CDS_4" ON "UniprotCDS" ("name","synonyms","ordered_locus_name","ORF_name");

COMMIT;
