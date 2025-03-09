# florentiaIllustrata_code
Project's repository for the ETL (Extract, Transform, Load) process of Florentia Illustrata project. 

Florentia Illustrata is a digital platform developed during an internship at I Tatti - The Harvard University Center for Italian Renaissance. This platform utilizes ResearchSpace to provide access to historical cadastral data of 19th-century Florence. The project's primary goal is to make complex cadastral information more accessible and comprehensible for researchers and the general public. The foundation of Florentia Illustrata is the Belli et al. (2022) dataset, which comprises digitized and georeferenced cadastral maps, along with descriptive tables detailing land parcels, ownership, toponymy, and land use.

A significant contribution of this research is the implementation of an ETL (Extract, Transform, Load) process to prepare the cadastral data. This process involved designing a data model using CIDOC CRM, which was then applied to create an RDF Knowledge Graph. The Knowledge Graph serves as the semantic structure of the Florentia Illustrata platform, enabling map visualization and semantic querying capabilities.

The project goes beyond mere spatial representation by linking cadastral data with historical narratives. Through Florentia Illustrata, users can uncover the stories of the people who lived and worked in 19th-century Florence, providing a multi-layered perspective on urban history as both physical space and lived experience. This approach not only facilitates historical research but also illustrates the potential of Semantic Web technologies in preserving and interpreting cultural heritage.

This project was carried out as part of an internship for thesis preparation within the Master's Degree in *Digital Humanities and Digital Knowledge* of the student Erica Andreose, at the University of Bologna. The thesis focused on *Knowledge Management*, specifically exploring the role of Semantic Web technologies in preserving and interpreting cultural heritage.

The internship and thesis work involved the design and implementation of an ETL pipeline to transform historical cadastral data into a structured RDF Knowledge Graph, enabling the integration of diverse datasets and facilitating deeper insights into historical urban life.

## Input files:

The input files of these scripts are part of the Belli et al. (2022) research output. References:

Belli, Gianluca, Fabio Lucchesi, and Paola Raggi. 2022. *Firenze nella prima metà dell’Ottocento: La città nei documenti del Catasto Generale Toscano*. Firenze: Firenze University Press. https://doi.org/10.36253/979-12-215-0002-8.

Firenze University Press, Redazione. 2023.“*Mappe*”. figshare.doi:10.6084/m9.figshare.23500524.v1.

Firenze University Press, Redazione. 2023.“*Banche Dati Geografiche*”. figshare.doi:10.6084/m9.figshare.23500503.v1.

Firenze University Press, Redazione. 2023.“*Banche Dati Alfanumeriche*”. figshare.doi:10.6084/m9.figshare.23500473.v1.

In particular, for the creation of the final Knowledge Graph were used the files:

-	“*Geodatabase_1_Parcellizzazione_Fondiaria.zip*” from “*Banche dati Geografiche*”
-	“*Tabella 1. Gli appezzamenti.csv*” from “*Banche Dati Alfanumeriche*”
-	“*Tabella 2. I proprietari.csv*” from “*Banche Dati Alfanumeriche*”


### macro_categories

This folder contains a Python script (*mapping_specie_pro.py*) for classifying land parcels from the 19th-century cadastral dataset into seven macro categories based on the "*specie pro*" property type column. The dataset, stored in a PostgreSQL database and accessed via pgAdmin, originally included 609+ detailed property types, making visualization difficult due to inconsistencies like synonyms and archaic terms.

To improve clarity, the *assign_macro_category* function automatically maps these values to broader macro categories using predefined dictionaries. The script outputs:

- *macro.csv* → Mapped "specie pro" values with their macro category
- *solo_nc.csv* → Unclassified values for manual review
  
The results are then injected into the PostgreSQL database via SQL INSERT, adding a new "macro" column for better data visualization. This classification complements the existing "*car_ediliz*" column, offering a more user-friendly interpretation of land use.

![snapshot-1738509120526@2x](https://github.com/user-attachments/assets/62546b31-4799-4105-b9d8-b378e81d5559)


### merge

This folder contains a Python script for merging and standardizing land parcel data from the original dataset. The process involves:

**1. Merging CSV Files**: "*Tabella 1. Gli Appezzamenti*" (land parcels) and "*Tabella 2. I Proprietari*" (owners) are combined using the "*ID Appezzamento*" column to create "*appezzamenti_proprietari*", which is stored in the PostgreSQL database at I Tatti.

**2.  Linking Geometry Data**: The "*parcellizzazione_fondiaria*" table (which contains WKT geometry) is connected to "*appezzamenti_proprietari*" using parcel identifiers. However, inconsistencies in parcel numbering required data cleaning.

**3. Cleaning and Standardization**: A new column ("*belli_id*") was added to "*parcellizzazione_fondiaria*" to store the standardized parcel identifiers, ensuring correct mapping to "*ID Appezzamento*." This allows accurate integration of spatial and descriptive data.

**4. Database Integration**: The cleaned and structured tables are now part of the PostgreSQL database and serve as a foundation for the Florentia Illustrata ResearchSpace instance, where users can visualize parcel data and retrieve ownership details.

![Column from parcellizzazione_fondiaria (4)](https://github.com/user-attachments/assets/97fcaf5a-3ea3-49e5-b114-e2eeae07b4f7)


### RDFfy

The RDFfy folder contains a Python script designed to convert the elaborated tabular data into an RDF Knowledge Graph based on the CIDOC-CRM ontology. 

It performs the following key functions:

**1. Data Transformation to RDF**

Reads tabular data (CSV format) containing cadastral records.
Maps each row to corresponding CIDOC-CRM entities and relationships.
Generates RDF triples in N-Triples (.nt) format for structured knowledge representation.

**2. CIDOC CRM-Based Knowledge Modeling**

Represents land parcels as *E24_Physical_Human_Made_Thing*, ensuring accurate classification. Tracks ownership history using *E8_Acquisition*, linking parcels to *E21_Person* (individual owners) or *E74_Group* (organizations).
Defines historical locations using *E53_Place*, recording civic addresses and spatial changes over time. Connects cadastral documents (*E31_Document*) to parcels through *E93_Presence*, ensuring historical accuracy.
Records parcel measurements (*E16_Measurement*, *E54_Dimension*) in original (*braccia quadrate fiorentine*) and converted (*square meters*) units. Assigns identifiers (*E42_Identifier*) and classification types (*E55_Type*) to each entity for structured metadata management.

![Data_model_FI drawio (7)](https://github.com/user-attachments/assets/6a7b00b9-8aea-469e-8cbe-c32f71c3031c)

**3. RDF Serialization**

Uses *rdflib* to generate RDF triples efficiently. 
The script overcomes rdflib’s Turtle serialization limitations by:
- First exporting the graph in N-Triples (.nt) format for faster processing.
- Then converting it to Turtle (.ttl) format using *rapper*.

#### Dependencies

To run the *RDFfy.py* script, install the required Python libraries:
- pandas: For handling and processing CSV data.
- rdflib: To generate and serialize RDF graphs in various formats (e.g., N-Triples, Turtle).
- re: For regular expression-based data cleaning (e.g., formatting of field values).
- subprocess: To run system commands, such as converting N-Triples to Turtle format.
  
You can install these dependencies using pip by running the following command:

```
pip install pandas rdflib
```

External Command-Line Tool:
- rapper: A command-line RDF tool for converting N-Triples to Turtle format. You will need to have rapper installed on your system.

To install rapper, follow the instructions depending on your operating system. For example, on Ubuntu you can use:
```
sudo apt-get install raptor2-utils
```

#### Usage

To use the RDFfy script to convert a CSV file into an RDF graph:

**1. Prepare your CSV file and modify the script**:
Ensure your CSV file contains cadastral records with the following fields (which should be consistent with your input data format):

ID_Appezzamento (Plot ID)
Cognome (Surname of the owner)
Nome (Name of the owner)
Ente (Entity or institution)
Volume, Carta, Sezione, Foglio (Document identifiers)
Superficie_braccia_quadrate (Area in traditional units)
Superficie_metri_quadrati (Area in square meters)
...
And other relevant fields related to cadastral data.

Modify and personalize the script in this section where you add the specific path of the input data:
```
csv_file_path = "merged_data_modified.csv" # modify with your input data path
```

**2. Run the Script**
Execute the script by running the following command in your terminal:

```
python rdffy.py
```

**3. Script Behavior**

The script will load the CSV data from the specific path (you can personalize it in the script if needed).
The script will then process each row, generating RDF triples that describe land parcels, ownership, locations, and other data points.
After processing, it will serialize the RDF graph into N-Triples (.nt) format, and the file will be saved in the same directory as the CSV file.
The N-Triples (.nt) file is then converted to Turtle (.ttl) format using the rapper command-line tool.

**4. Output**
   
After the script runs, you will see the following output:

  - An N-Triples (.nt) file (e.g., *output_data.nt*).
  - A Turtle (.ttl) file (e.g., *output_data_converted_final.ttl*).
  - 
These files will contain the RDF representation of the cadastral data and can be loaded into an RDF store like [Blazegraph](https://blazegraph.com/) or [Qlever](https://github.com/ad-freiburg/qlever).

#### Notes

The script assumes the CSV file is formatted with semicolons (;) as delimiters.
You can customize the CSV file path and modify the script accordingly if your file has a different structure or delimiter.

#### Example Output

A sample RDF triple from the turtle version of the generated graph:

```
<https://florentiaillustrata.net/resource/appezzamento/705>
    crm:P101_has_as_general_use <https://florentiaillustrata.net/resource/uso/bottega> ;
    crm:P1_is_identified_by <https://florentiaillustrata.net/resource/appezzamen/628>, <https://florentiaillustrata.net/resource/art_di_stima/390>, <https://florentiaillustrata.net/resource/belli_id/705>, <https://florentiaillustrata.net/resource/carta/26v>, <https://florentiaillustrata.net/resource/foglio/1>, <https://florentiaillustrata.net/resource/num_del_campione/1683>, <https://florentiaillustrata.net/resource/sezione/E>, <https://florentiaillustrata.net/resource/volume/3> ;
    crm:P24i_changed_ownership_through <https://florentiaillustrata.net/resource/appezzamento/705/acquisition> ;
    crm:P2_has_type crm:E24_Physical_Human_Made_Thing, <https://florentiaillustrata.net/resource/specie_pro/bottega> ;
    crm:P43_has_dimension <https://florentiaillustrata.net/resource/dimension_bqf/235.0>, <https://florentiaillustrata.net/resource/dimension_mq/80.041> ;
    crm:P53_has_former_or_current_location <https://florentiaillustrata.net/resource/appezzamento/705/place> .
```

The output generated Knowledge Graph produced with this script for the Florentia Illustrata project is stored in AMS Acta:
[https://amsacta.unibo.it/id/eprint/8236](https://amsacta.unibo.it/id/eprint/8236)

## SPARQL Queries example

1. Retrieve street addresses, civic number and owner name of the land parcels:

```
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?appezzamento ?civic_number ?street_name ?owner_label WHERE {
  # Retrieve only parcels that have use = "macelleria"
  ?appezzamento crm:P101_has_as_general_use <https://florentiaillustrata.net/resource/uso/macelleria> .

  # Find the location of these parcels
  ?appezzamento crm:P53_has_former_or_current_location ?location .


  # Retrieve civic number
  OPTIONAL {
    ?location crm:P1_is_identified_by ?civic_identifier .
    ?civic_identifier crm:P2_has_type <https://florentiaillustrata.net/resource/num_civico> .
    ?civic_identifier rdfs:label ?civic_number .
  }

  # Retrieve street name (toponomastica)
  OPTIONAL {
    ?location crm:P1_is_identified_by ?street_identifier .
    ?street_identifier crm:P2_has_type <https://florentiaillustrata.net/resource/toponomastica> .
    ?street_identifier rdfs:label ?street_name .
  }

  # Retrieve the owner of the "macelleria" parcel
  OPTIONAL {
    ?appezzamento crm:P24i_changed_ownership_through ?acquisition_event .
    ?owner crm:P22i_acquired_title_through ?acquisition_event .
    ?owner rdfs:label ?owner_label .
  }
}
```

2. Retrieve the Top Ten Major Landowners

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?acquisition ?proprietario (SUM(?mq) AS ?totalSuperficie) WHERE {
  ?appezzamento crm:P2_has_type crm:E24_Physical_Human_Made_Thing ;
                crm:P24i_changed_ownership_through ?acquisition ;
                crm:P43_has_dimension ?dimension .

  ?dimension crm:P2_has_type crm:E54_Dimension ;
             crm:P91_has_unit <https://florentiaillustrata.net/resource/metri_quadrati> ;
             rdfs:label ?superficie .

  BIND(xsd:decimal(?superficie) AS ?mq)

  # Ensuring only persons are selected as proprietors
  ?ente crm:P22i_acquired_title_through ?acquisition ;
        crm:P2_has_type crm:E21_Person ;
        rdfs:label ?proprietario .
}
GROUP BY ?acquisition ?proprietario
ORDER BY DESC(?totalSuperficie)
LIMIT 10
```

3. Retrive the civic number, the street adress and the owner's name of the land parcels that has typology "butcher shop"
   
```
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?appezzamento ?civic_number ?street_name ?owner_label WHERE {
  # Retrieve only parcels that have use = "macelleria"
  ?appezzamento crm:P101_has_as_general_use <https://florentiaillustrata.net/resource/uso/macelleria> .

  # Find the location of these parcels
  ?appezzamento crm:P53_has_former_or_current_location ?location .


  # Retrieve civic number
  OPTIONAL {
    ?location crm:P1_is_identified_by ?civic_identifier .
    ?civic_identifier crm:P2_has_type <https://florentiaillustrata.net/resource/num_civico> .
    ?civic_identifier rdfs:label ?civic_number .
  }

  # Retrieve street name (toponomastica)
  OPTIONAL {
    ?location crm:P1_is_identified_by ?street_identifier .
    ?street_identifier crm:P2_has_type <https://florentiaillustrata.net/resource/toponomastica> .
    ?street_identifier rdfs:label ?street_name .
  }

  # Retrieve the owner of the "macelleria" parcel
  OPTIONAL {
    ?appezzamento crm:P24i_changed_ownership_through ?acquisition_event .
    ?owner crm:P22i_acquired_title_through ?acquisition_event .
    ?owner rdfs:label ?owner_label .
  }
}
```

## The Florentia Illustrata process

The following figure summarizes the key steps of the whole Florentia Illustrata project:

**1. ETL Process and Relational Database**

The tabular datasets go through an ETL process (*mapping_specie_pro.py* and *check_merging_parc.py*) and are stored in a PostgreSQL relational database on the I Tatti server.

**2. Data Modeling with CIDOC CRM and transformation process**

Using the same processed data, a data model is created based on the CIDOC CRM 7.1 ontology to structure the information according to semantic web standards.
The data is processed by a Python script (*RDFfy.py*), which follows the guidelines from the data model to create RDF triples and serialize them into a Turtle RDF file, forming the Florentia Illustrata knowledge graph.

**3. Uploading the Knowledge Graph to Blazegraph in ResearchSpace**

The knowledge graph is uploaded to the Blazegraph triplestore within the ResearchSpace instance created for the project (www.florentiaillustrata.net). From here, the data can be queried and linked using SPARQL to templates and functionalities available in ResearchSpace.

**4. Integration with the Relational Database for Spatial Data**

ResearchSpace also remains connected to the relational SQL database via SAIL, allowing it to retrieve WKT geometry values for land parcels and link them to their descriptive data.

![florentia_schema](https://github.com/user-attachments/assets/f6553354-57f0-47e6-8527-991c0258bd2c)




