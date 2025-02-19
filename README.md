# florentiaIllustrata_code
Project's repository for the ETL (Extract, Transform, Load) process of Florentia Illustrata project. 

Florentia Illustrata is a digital platform developed during an internship at I Tatti - The Harvard University Center for Italian Renaissance. This platform utilizes ResearchSpace to provide access to historical cadastral data of 19th-century Florence. The project's primary goal is to make complex cadastral information more accessible and comprehensible for researchers and the general public. The foundation of Florentia Illustrata is the Belli et al. (2022) dataset, which comprises digitized and georeferenced cadastral maps, along with descriptive tables detailing land parcels, ownership, toponymy, and land use.

A significant contribution of this research is the implementation of an ETL (Extract, Transform, Load) process to prepare the cadastral data. This process involved designing a data model using CIDOC CRM, which was then applied to create an RDF Knowledge Graph. The Knowledge Graph serves as the semantic structure of the Florentia Illustrata platform, enabling map visualization and semantic querying capabilities.

The project goes beyond mere spatial representation by linking cadastral data with historical narratives. Through Florentia Illustrata, users can uncover the stories of the people who lived and worked in 19th-century Florence, providing a multi-layered perspective on urban history as both physical space and lived experience. This approach not only facilitates historical research but also illustrates the potential of Semantic Web technologies in preserving and interpreting cultural heritage.

## Folders:

### data
Folder with the starting csv data "Tabella 1. Gli appezzamenti.csv", "Tabella 2. I proprietari.csv" and the gis dataset "Parcellizzazione fondiaria.shp".
All these files are part of the Belli et al. (2022) research output. References:
Belli, Gianluca, Fabio Lucchesi, and Paola Raggi. 2022. Firenze nella prima metà dell’Ottocento: La città nei documenti del Catasto Generale Toscano. Firenze: Firenze University Press. https://doi.org/10.36253/979-12-215-0002-8.

Firenze University Press, Redazione. 2023.“Mappe”.figshare.doi:10.6084/m9.figshare.23500524.v1.

Firenze University Press, Redazione. 2023.“Banche Dati Geografiche”.figshare.doi:10.6084/m9.figshare.23500503.v1.

Firenze University Press, Redazione. 2023.“Banche Dati Alfanumeriche”.figshare.doi:10.6084/m9.figshare.23500473.v1.

Inside the sub-folder "output" some of the output csv files created with the scripts present in the repo.

### macro_categories

Scripts for the 
![snapshot-1738876367031@2x](https://github.com/user-attachments/assets/9cf5c9a8-e753-4292-a60d-c33fde3e2244)

RDF: https://amsacta.unibo.it/id/eprint/8236
![Column from parcellizzazione_fondiaria (4)](https://github.com/user-attachments/assets/70bbc19b-0ea4-43f3-9d2f-e39ba0574ae0)

### RDFfy

![Data_model_FI drawio (7)](https://github.com/user-attachments/assets/cc8c60e8-bf42-443a-beb1-78fe4033c4ea)


![florentia_schema](https://github.com/user-attachments/assets/67aa3a99-a122-4e1f-a62a-e1b7821aceee)


