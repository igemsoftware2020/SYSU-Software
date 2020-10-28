### run

```bash
python app.py
```

### interface

```json
//response format

// success
{
    "response": "...",
    "status": 1,
    "message": "success"
}

// fail
{
    "response": "...",
    "status": 0,
    "message": // error_message
}
```

#### 根据TF名字查询元件

##### URL:

```http
/api/element/tf=<tf_name>
```

##### METHOD: GET

##### EXAMPLE:

```json
http://127.0.0.1:5000/api/element/tf=CRP-Sxy

{
    "message": "success",
    "response": [
        "crp",
        "sxy"
    ],
    "status": 1
}
```

#### 

#### 元件总数查询

##### URL:

```http
/api/element/totalsize
```

##### METHOD: GET

##### EXAMPLE:

```json
http://127.0.0.1:5000/api/element/totalsize

{
    "message": "success",
    "response": "33007",
    "status": 1
}
```

#### 元件列表查询

##### URL

```http
/api/element/elementlist/offset=<offset>&num=<num>

返回从offset开始的num个元件的基本信息
```

##### METHOD

GET

##### EXAMPLE

```json
http://127.0.0.1:5000/api/element/elementlist/offset=40&num=5

{
    "message": "success",
    "response": {
        "BBa_B0070": {
            "creator": "Barry Canton",
            "displayId": "BBa_B0070",
            "mutableDescription": "This RBS has the modified Shine-Dalgarno sequence, it has a reduced secondary structure relative to using the actual Brink sequence with mixed connective sites flanking it.  the spacing between the SD and the ATG is the same as that used by Brink et al. even though it is non-optimal for <I>E. coli</I>",
            "role": [
                "ribosome_entry_site",
                "RBS"
            ]
        },
        "BBa_B0071": {
            "creator": "Barry Canton",
            "displayId": "BBa_B0071",
            "mutableDescription": "This RBS has the modified Shine-Dalgarno sequence, it has a reduced secondary structure relative to using the actual Brink sequence with mixed connective sites flanking it.    This RBS is modified from B0071 by reducing the 3' sequence so that the SD to ATG spacing is closer to that which is optimal for <I>E. coli</I>.",
            "role": [
                "ribosome_entry_site",
                "RBS"
            ]
        },
        "BBa_B0072": {
            "creator": "Bartholomew Canton",
            "displayId": "BBa_B0072",
            "mutableDescription": "-- No description --",
            "role": [
                "ribosome_entry_site",
                "RBS"
            ]
        },
        "BBa_B0073": {
            "creator": "Bartholomew Canton",
            "displayId": "BBa_B0073",
            "mutableDescription": "-- No description --",
            "role": [
                "RBS",
                "ribosome_entry_site"
            ]
        },
        "BBa_B0074": {
            "creator": "Bartholomew Canton",
            "displayId": "BBa_B0074",
            "mutableDescription": "-- No description --",
            "role": [
                "ribosome_entry_site",
                "RBS"
            ]
        }
    },
    "status": 1
}
```



#### 元件查询

##### URL:

```http
/api/element/like/name=<name>&rolefilter=<filter_list>&limit=<limit_num>
/api/element/fuzzy/name=<name>&rolefilter=<filter_list>&limit=<limit_num>

name: 模糊匹配，只需要输入部分的名称
limit_num: 最多找多少个符合条件的元件
rolefilter: 若干个role，用-连接，只选择这些role的元件 e.g. CDS-RBS（必须是CDS或者是RBS）

输出会按照匹配分数从高到低排列
```

```http
/api/element/like/name=<name>&limit=<limit_num>
/api/element/fuzzy/name=<name>&limit=<limit_num>

name: 模糊匹配，只需要输入部分的名称
limit_num: 最多找多少个符合条件的元件

输出会按照匹配分数从高到低排列
```



##### METHOD: GET

##### EXAMPLE:

```json
http://127.0.0.1:5000/api/element/name=0024&rolefilter=CDS-RBS&limit=10


{
    "message": "success",
    "response": {
        "BBa_C0024": {
            "created": "2004-08-01T11:00:00Z",
            "creator": "MIT SBC 2004 (Ken)",
            "description": null,
            "displayId": "BBa_C0024",
            "modified": "2015-08-31T04:07:23Z",
            "mutableDescription": "CheB is part of the chemotaxis pathway in E. coli.",
            "mutableNotes": "Checked (DE, VC, KN).  Part ready for synthesis.  8/3/4",
            "mutableProvenance": "NCBI - E. Coli strain K12 substrain MG1655",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_C0024",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "cheB",
            "topLevel": "https://synbiohub.org/public/igem/BBa_C0024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_C0024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_C2002": {
            "created": "2006-05-31T11:00:00Z",
            "creator": "Reshma Shetty",
            "description": null,
            "displayId": "BBa_C2002",
            "modified": "2015-08-31T04:07:25Z",
            "mutableDescription": null,
            "mutableNotes": null,
            "mutableProvenance": null,
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_C2002",
            "role": [
                "Coding",
                "CDS"
            ],
            "title": "BBa_C2002",
            "topLevel": "https://synbiohub.org/public/igem/BBa_C2002/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_C2002",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_I51002": {
            "created": "2006-05-11T11:00:00Z",
            "creator": "Sean Milton",
            "description": null,
            "displayId": "BBa_I51002",
            "modified": "2015-08-31T04:07:42Z",
            "mutableDescription": null,
            "mutableNotes": null,
            "mutableProvenance": null,
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_I51002",
            "role": [
                "Coding",
                "CDS"
            ],
            "title": "BBa_I51002",
            "topLevel": "https://synbiohub.org/public/igem/BBa_I51002/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_I51002",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_I712002": {
            "created": "2007-10-20T11:00:00Z",
            "creator": "Andrej Ondracka",
            "description": null,
            "displayId": "BBa_I712002",
            "modified": "2015-08-31T04:07:45Z",
            "mutableDescription": "Chemokine (C-C motif) receptor 5, a HIV-1 co-receptor.",
            "mutableNotes": "The part is cloned into BBa_J52017, a vector with eukaryontic terminator. PstI and EcoRI restriction sites inside CCR5 gene were mutated.",
            "mutableProvenance": "CCR5 gene was obtained from Origene.",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_I712002",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "BBa_I712002",
            "topLevel": "https://synbiohub.org/public/igem/BBa_I712002/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_I712002",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_J70024": {
            "created": "2008-10-19T11:00:00Z",
            "creator": "Tom Knight",
            "description": null,
            "displayId": "BBa_J70024",
            "modified": "2015-05-08T01:08:20Z",
            "mutableDescription": "The tetM antibiotic resistance gene synthesized by Geneart from a protein sequence derived from the Ureaplasma urealyticum tetM gene.  Synthesized with a compromise codon usage table for expression in both E. coli and Mesoplasma florum.  Highly active in both E. coli and Mesoplasma florum.",
            "mutableNotes": "Elimination of restriction sites, CGG codons, UGA codons, rare codons in both species.",
            "mutableProvenance": "Synthesized from the Ureaplasma urealyticum tetM gene sequence, with recoding.",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_J70024",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "BBa_J70024",
            "topLevel": "https://synbiohub.org/public/igem/BBa_J70024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_J70024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_K120024": {
            "created": "2008-10-29T12:00:00Z",
            "creator": "Lu Yuanye",
            "description": null,
            "displayId": "BBa_K120024",
            "modified": "2015-05-08T01:09:40Z",
            "mutableDescription": "hAIDsc is optimized in yeast codon.",
            "mutableNotes": "it can turn C to U",
            "mutableProvenance": "it`s from human B cell line and recode in yeast codon by Youri I Pavlov",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_K120024",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "BBa_K120024",
            "topLevel": "https://synbiohub.org/public/igem/BBa_K120024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_K120024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_K1640024": {
            "created": "2015-09-17T11:00:00Z",
            "creator": "Meghan Cook",
            "description": null,
            "displayId": "BBa_K1640024",
            "modified": "2015-09-18T12:20:25Z",
            "mutableDescription": "n/a",
            "mutableNotes": "n/a",
            "mutableProvenance": "n/a",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_K1640024",
            "role": [
                "Coding",
                "CDS"
            ],
            "title": "BBa_K1640024",
            "topLevel": "https://synbiohub.org/public/igem/BBa_K1640024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_K1640024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_K590024": {
            "created": "2011-09-14T11:00:00Z",
            "creator": "Sydney Gordon, Daniel Hadidi, Elizabeth Stanley, Sarah Wolf, Angus Toland, Sean Wu",
            "description": null,
            "displayId": "BBa_K590024",
            "modified": "2015-05-08T01:12:48Z",
            "mutableDescription": "A mutated Kumamolisin-As enzyme aimed to combat celiac disease by increased specificity for the PQLP peptide, an antigenic epitope in gliadin.",
            "mutableNotes": "Point mutation at residues 354, 358, and 368 from Serine to Asparagine, Aspartate to Glycine, and Aspartate to Histidine, respectively.",
            "mutableProvenance": "In-House Mutant",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_K590024",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "S354N_Tri",
            "topLevel": "https://synbiohub.org/public/igem/BBa_K590024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_K590024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_M10024": {
            "created": "2009-05-08T11:00:00Z",
            "creator": "Hank Shih",
            "description": null,
            "displayId": "BBa_M10024",
            "modified": "2015-05-08T01:13:51Z",
            "mutableDescription": "TBA",
            "mutableNotes": "Construction of {a~Inv-native>} basic part\nPCR Bhs001F/Bhs002R on E. coli strain 0157:H7     (146 bp, gp = A)\nPCR Bhs002F/Bhs003R on E. coli strain 0157:H7     (1889 bp, gp = B)\n----------------------------\nPCR Bhs001F/Bhs003R on A+B                       (2009 bp, EcoRI/BamHI)\nDigest pBca9495CA-Bca1144#5                      (EcoRI/BamHI, 3039+910, L)\nProduct is pBca9495CA-M10024                     {a~Inv-native>}\n----------------------------\nBhs001F  Forward EcoRI for {a~Inv-native>}          cccaaGAATTCatgAGATCTtaacATGATTACTCATGGTTG\nBhs002F  Removing the EcoRI site from {a~Inv-native>}   GTTAATCAGAACTCATTTGCAAATGG\nBhs002R  Removing the EcoRI site from {a~Inv-native>}  CCATTTGCAAATGAGTTCTGATTAAC\nBhs003R  Reverse BamHI for {a~Inv-native>}          GCAAAggatccGGCCTTGGTTTGATCAAAAAATATAACCGCAC",
            "mutableProvenance": "Genomic sequence of E. coli strain 0157:H7",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_M10024",
            "role": [
                "CDS",
                "Coding"
            ],
            "title": "BBa_M10024",
            "topLevel": "https://synbiohub.org/public/igem/BBa_M10024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_M10024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        },
        "BBa_M50024": {
            "created": "2016-10-26T11:00:00Z",
            "creator": "James Benjami Hu",
            "description": null,
            "displayId": "BBa_M50024",
            "modified": "2016-10-27T07:29:30Z",
            "mutableDescription": "asdf",
            "mutableNotes": "asdf",
            "mutableProvenance": "asdf",
            "persistentIdentity": "https://synbiohub.org/public/igem/BBa_M50024",
            "role": [
                "ribosome_entry_site",
                "RBS"
            ],
            "title": "BBa_M50024",
            "topLevel": "https://synbiohub.org/public/igem/BBa_M50024/1",
            "type": "http://www.biopax.org/release/biopax-level3.owl#DnaRegion",
            "version": "1",
            "wasDerivedFrom": "http://parts.igem.org/Part:BBa_M50024",
            "wasGeneratedBy": "https://synbiohub.org/public/igem/igem2sbol/1"
        }
    },
    "status": 1
}
```



#### 插入元件

##### URL

```http
/api/element/add
```

##### METHOD

POST

##### BODY

格式请见doc/addElement.jsonc

example文件是doc/addElement-example.json

#### 图搜索

##### URL

```http
/api/gene-circuit/search/mode=<mode>&limit=<limit>

mode = <structure-rstructure-element-relement>, 4选n

e.g. /api/gene-circuit/search/mode=rstructure&limit=5
```

##### METHOD

POST

##### BODY

格式请见roadmapSearch/doc/BBa_B3202.json

#### 元件更新

**只能更新用户自己添加的元件**

##### URL

```http
/api/element/modify/displayId=<displayId>
```

##### METHOD

PUT

##### EXAMPLE

```http
http://127.0.0.1:5000/api/element/modify/displayId=BBa_B3202_test5
```

#### 元件删除

**只能删除用户自己添加的元件**

##### URL

```http
/api/element/delete/displayId=<displayId> 
```

##### METHOD

DELETE
