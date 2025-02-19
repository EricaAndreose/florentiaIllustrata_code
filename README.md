# florentiaIllustrata_code
Project's repository for the ETL (Extract, Transform, Load) process of Florentia Illustrata project. 

Florentia Illustrata is a digital platform developed during an internship at I Tatti - The Harvard University Center for Italian Renaissance. This platform utilizes ResearchSpace to provide access to historical cadastral data of 19th-century Florence. The project's primary goal is to make complex cadastral information more accessible and comprehensible for researchers and the general public. The foundation of Florentia Illustrata is the Belli et al. (2022) dataset, which comprises digitized and georeferenced cadastral maps, along with descriptive tables detailing land parcels, ownership, toponymy, and land use.

A significant contribution of this research is the implementation of an ETL (Extract, Transform, Load) process to prepare the cadastral data. This process involved designing a data model using CIDOC CRM, which was then applied to create an RDF Knowledge Graph. The Knowledge Graph serves as the semantic structure of the Florentia Illustrata platform, enabling map visualization and semantic querying capabilities.

The project goes beyond mere spatial representation by linking cadastral data with historical narratives. Through Florentia Illustrata, users can uncover the stories of the people who lived and worked in 19th-century Florence, providing a multi-layered perspective on urban history as both physical space and lived experience. This approach not only facilitates historical research but also illustrates the potential of Semantic Web technologies in preserving and interpreting cultural heritage.

## Input files:

The input files of these scripts are part of the Belli et al. (2022) research output. References:
Belli, Gianluca, Fabio Lucchesi, and Paola Raggi. 2022. Firenze nella prima metà dell’Ottocento: La città nei documenti del Catasto Generale Toscano. Firenze: Firenze University Press. https://doi.org/10.36253/979-12-215-0002-8.

Firenze University Press, Redazione. 2023.“Mappe”.figshare.doi:10.6084/m9.figshare.23500524.v1.

Firenze University Press, Redazione. 2023.“Banche Dati Geografiche”.figshare.doi:10.6084/m9.figshare.23500503.v1.

Firenze University Press, Redazione. 2023.“Banche Dati Alfanumeriche”.figshare.doi:10.6084/m9.figshare.23500473.v1.

In particular the csv data "Tabella 1. Gli appezzamenti.csv", "Tabella 2. I proprietari.csv" and the gis dataset "Parcellizzazione fondiaria.shp".

### macro_categories
![snapshot-1738509120526@2x](https://github.com/user-attachments/assets/62546b31-4799-4105-b9d8-b378e81d5559)

Scripts for the 
![Column from parcellizzazione_fondiaria (4)](https://github.com/user-attachments/assets/97fcaf5a-3ea3-49e5-b114-e2eeae07b4f7)


RDF: https://amsacta.unibo.it/id/eprint/8236
![florentia_schema](https://github.com/user-attachments/assets/f6553354-57f0-47e6-8527-991c0258bd2c)


### RDFfy
![Data_model_FI drawio (7)](https://github.com/user-attachments/assets/6a7b00b9-8aea-469e-8cbe-c32f71c3031c)




