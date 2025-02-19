# -*- coding: utf-8 -*-
# Copyright (c) 2024,
# Erica Andreose
# Remo Grillo
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONrCT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.


import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace, RDFS
from rdflib.namespace import XSD
import os
import re
import time
total_time = time.time()
loop_start_time = time.time()


CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

BASE = Namespace("https://florentiaillustrata.net/resource/")


g = Graph()
g.bind("crm", CRM)
g.bind("base", BASE)


csv_file_path = "merged_data_modified.csv"
data = pd.read_csv(csv_file_path, delimiter=";")

# Rename columns 
data.columns = data.columns.str.replace(r'\W+', '_', regex=True).str.strip('_')
print(data.columns.tolist())



document_uri = BASE["cadastrial_document_1834"]
place_uri = BASE["place/Florence"]
measurements_appezzamento_uri = BASE["cadastrial_survey"]
timespan_uri = BASE["cadastrial_survey/timespan"]
appez_uri = BASE["appezzamento"]




match_digit_pattern = re.compile(r"(\d+)")
sub_space_pattern = re.compile(r'\s+')
sub_non_alnum_pattern = re.compile(r'[^\w\s-]')



# document_uri 
g.add((document_uri, CRM["P2_has_type"], CRM["E31_Document"]))
g.add((document_uri, CRM["P3_has_note"], Literal("Florence cadastral data 1834", datatype=XSD.string)))
g.add((document_uri, CRM["P70_documents"], measurements_appezzamento_uri))
g.add((document_uri, CRM["P129_is_about"], place_uri))

# place_uri
g.add((place_uri, CRM["P2_has_type"], CRM["E53_Place"]))
g.add((place_uri, CRM["P3_has_note"], Literal("Florence", datatype=XSD.string)))

# measurements_appezzamento_uri 
g.add((measurements_appezzamento_uri, CRM["P2_has_type"], CRM["E16_Measurement"]))
g.add((measurements_appezzamento_uri, CRM["P4_has_time_span"], timespan_uri))

# timespan_uri 
g.add((timespan_uri, CRM["P2_has_type"], CRM["E52_Time-Span"]))

# appez_uri note
g.add((appez_uri, CRM["P3_has_note"], Literal(
    "appezzamento: transcription of the identification number reported in the maps of the plot to which the polygon refers.", datatype=XSD.string)))



for record in data.itertuples(index=False):


    id_appezzamento = record.ID_Appezzamento
    cognome = record.Cognome
    nome = record.Nome
    patronimico = record.Patronimico
    ente = record.Ente
    moglie_di = getattr(record, 'Moglie_di', None)
    volume = record.Volume
    carta = record.Carta
    sezione = record.Sezione
    foglio = record.Foglio
    appezzamento = record.Appezzamento
    art_di_stima = getattr(record, 'Articolo_di_stima', None)
    num_del_campione = getattr(record, 'Numero_del_campione', None)
    specie_pro = getattr(record, 'Specie_della_proprieta', None)
    sup_bqf = getattr(record, 'Superficie_braccia_quadrate', None)
    sup_mq = getattr(record, 'Superficie_metri_quadrati', None)
    toponomastica = record.Toponomastica
    titolo = record.Titolo
    num_civico = getattr(record, 'Numero_civico', None)
    uso = record.Uso

    appezzamento_uri = BASE[f"appezzamento/{id_appezzamento}"]


    triples = []

    # appezzamento
    triples.append((appezzamento_uri, CRM["P2_has_type"], CRM["E24_Physical_Human_Made_Thing"]))


    if id_appezzamento and not pd.isna(id_appezzamento):

        presence_uri = BASE[f"appezzamento/{id_appezzamento}/presence"]
        acquisition_appezzamento_uri = BASE[f"appezzamento/{id_appezzamento}/acquisition"]
        place_appezzamento_uri = BASE[f"appezzamento/{id_appezzamento}/place"]
        belli_id = BASE[f"belli_id/{id_appezzamento}"]

        triples.append((document_uri, CRM["P70_documents"], presence_uri))

        # presence_uri 
        triples.append((presence_uri, CRM["P2_has_type"], CRM["E93_Presence"]))
        triples.append((presence_uri, CRM["P164_is_temporally_specified_by"], timespan_uri))
        triples.append((presence_uri, CRM["P197_covers_parts_of"], place_uri))
        triples.append((presence_uri, CRM["P195_was_a_presence_of"], appezzamento_uri))

        triples.append((appezzamento_uri, CRM["P24i_changed_ownership_through"], acquisition_appezzamento_uri))
        triples.append((acquisition_appezzamento_uri, CRM["P2_has_type"], CRM["E8_Acquisition"]))

        triples.append((appezzamento_uri, CRM["P53_has_former_or_current_location"], place_appezzamento_uri))
        triples.append((place_appezzamento_uri, CRM["P2_has_type"], CRM["E53_Place"]))

        triples.append((appezzamento_uri, CRM["P1_is_identified_by"], belli_id))
        triples.append((belli_id, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((belli_id, RDFS["label"], Literal(id_appezzamento, datatype=XSD.string)))


        

    if appezzamento and not pd.isna(appezzamento):

        match = match_digit_pattern.match(str(appezzamento))
        if match:
            appezzamento_value = match.group(1)

            appezzamento_appezzamento_uri = BASE[f"appezzamen/{appezzamento_value}"]

            triples.append((appezzamento_uri, CRM["P1_is_identified_by"], appezzamento_appezzamento_uri))
            triples.append((appezzamento_appezzamento_uri, RDFS["label"], Literal(appezzamento_value, datatype=XSD.string)))

            triples.append((appezzamento_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
            triples.append((appezzamento_appezzamento_uri, CRM["P2_has_type"], appez_uri))



    if foglio and not pd.isna(foglio):
        foglio_appezzamento_uri = BASE[f"foglio/{foglio}"]
        foglio_appezzamento_foglio_uri = BASE["foglio"]

        triples.append((appezzamento_uri, CRM["P1_is_identified_by"], foglio_appezzamento_uri))
        triples.append((foglio_appezzamento_uri, RDFS["label"], Literal(foglio, datatype=XSD.string)))

        triples.append((foglio_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((foglio_appezzamento_uri, CRM["P2_has_type"], foglio_appezzamento_foglio_uri))
        triples.append((foglio_appezzamento_foglio_uri, RDFS["label"], Literal("foglio", datatype=XSD.string)))
        triples.append((foglio_appezzamento_foglio_uri, CRM["P3_has_note"], Literal("foglio: cadastral section sheet.", datatype=XSD.string)))

    if specie_pro and not pd.isna(specie_pro):

        specie_pro_value = sub_space_pattern.sub('_', str(specie_pro).strip())
        specie_pro_appezzamento_uri = BASE[f"specie_pro/{specie_pro_value}"]
        specie_pro_appezzamento_sp_uri = BASE["specie_pro"]

        triples.append((appezzamento_uri, CRM["P2_has_type"], specie_pro_appezzamento_uri))
        triples.append((specie_pro_appezzamento_uri, RDFS["label"], Literal(specie_pro, datatype=XSD.string)))
        triples.append((specie_pro_appezzamento_uri, CRM["P2_has_type"], CRM["E55_Type"]))
        triples.append((specie_pro_appezzamento_uri, CRM["P2_has_type"], specie_pro_appezzamento_sp_uri))
        triples.append((specie_pro_appezzamento_sp_uri, RDFS["label"], Literal("specie_pro", datatype=XSD.string)))
        triples.append((specie_pro_appezzamento_sp_uri, CRM["P3_has_note"], Literal("specie_pro: species of the property of the plot to which the polygon refers as highlighted in the cadastral tables.", datatype=XSD.string)))


    if uso and not pd.isna(uso):
        uso_value = sub_space_pattern.sub('_', str(uso).strip())
        uso_appezzamento_uri = BASE[f"uso/{uso_value}"]
        uso_appezzamento_uso_uri = BASE["uso"]

        triples.append((appezzamento_uri, CRM["P101_has_as_general_use"], uso_appezzamento_uri))
        triples.append((uso_appezzamento_uri, RDFS["label"], Literal(uso, datatype=XSD.string)))

        triples.append((uso_appezzamento_uri, CRM["P2_has_type"], CRM["E55_Type"]))
        triples.append((uso_appezzamento_uri, CRM["P2_has_type"], uso_appezzamento_uso_uri))
        triples.append((uso_appezzamento_uso_uri, RDFS["label"], Literal("uso", datatype=XSD.string)))
        triples.append((uso_appezzamento_uso_uri, CRM["P3_has_note"], Literal("uso: description of commercial or productive activity carried out in the space of the plot as per the appraisal tables.", datatype=XSD.string)))

    if sezione and not pd.isna(sezione):
        sezione_appezzamento_uri = BASE[f"sezione/{sezione}"]
        sezione_appezzamento_sez_uri = BASE["sezione"]

        triples.append((appezzamento_uri, CRM["P1_is_identified_by"], sezione_appezzamento_uri))
        triples.append((sezione_appezzamento_uri, RDFS["label"], Literal(sezione, datatype=XSD.string)))

        triples.append((sezione_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((sezione_appezzamento_uri, CRM["P2_has_type"], sezione_appezzamento_sez_uri))
        triples.append((sezione_appezzamento_sez_uri, RDFS["label"], Literal("sezione", datatype=XSD.string)))
        triples.append((sezione_appezzamento_sez_uri, CRM["P3_has_note"], Literal("sezione: cadastral section of the plot whose polygon is referred to.", datatype=XSD.string)))

    if carta and not pd.isna(carta):
        carta_appezzamento_uri = BASE[f"carta/{carta}"]
        carta_appezzamento_carta_uri = BASE["carta"]

        triples.append((appezzamento_uri, CRM["P1_is_identified_by"], carta_appezzamento_uri))
        triples.append((carta_appezzamento_uri, RDFS["label"], Literal(carta, datatype=XSD.string)))

        triples.append((carta_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((carta_appezzamento_uri, CRM["P2_has_type"], carta_appezzamento_carta_uri))
        triples.append((carta_appezzamento_carta_uri, RDFS["label"], Literal("carta", datatype=XSD.string)))
        triples.append((carta_appezzamento_carta_uri, CRM["P3_has_note"], Literal("carta: placement in the register.", datatype=XSD.string)))

    if num_del_campione and not pd.isna(num_del_campione):
        match = match_digit_pattern.match(str(num_del_campione))
        if match:
            num_del_campione_value = match.group(1)
            num_del_campione_uri = BASE[f"num_del_campione/{num_del_campione_value}"]
            num_del_campione_ndc_uri = BASE["num_del_campione"]

            triples.append((appezzamento_uri, CRM["P1_is_identified_by"], num_del_campione_uri))
            triples.append((num_del_campione_uri, RDFS["label"], Literal(num_del_campione_value, datatype=XSD.string)))

            triples.append((num_del_campione_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
            triples.append((num_del_campione_uri, CRM["P2_has_type"], num_del_campione_ndc_uri))
            triples.append((num_del_campione_ndc_uri, RDFS["label"], Literal("num_del_campione", datatype=XSD.string)))
            triples.append((num_del_campione_ndc_uri, CRM["P3_has_note"], Literal("num_del_campione: transcription of the reference to the sample number where the lot of goods registered to the owner of the plot is located.", datatype=XSD.string)))

    if art_di_stima and not pd.isna(art_di_stima):
        match = match_digit_pattern.match(str(art_di_stima))
        if match:
            art_di_stima_value = match.group(1)
            art_di_stima_uri = BASE[f"art_di_stima/{art_di_stima_value}"]
            art_di_stima_ads_uri = BASE["art_di_stima"]

            triples.append((appezzamento_uri, CRM["P1_is_identified_by"], art_di_stima_uri))
            triples.append((art_di_stima_uri, RDFS["label"], Literal(art_di_stima_value, datatype=XSD.string)))

            triples.append((art_di_stima_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
            triples.append((art_di_stima_uri, CRM["P2_has_type"], art_di_stima_ads_uri))
            triples.append((art_di_stima_ads_uri, RDFS["label"], Literal("art_di_stima", datatype=XSD.string)))
            triples.append((art_di_stima_ads_uri, CRM["P3_has_note"], Literal("art_di_stima: number assigned to the real estate property during the appraisal operation (it can be the same for more parcels).", datatype=XSD.string)))

    if volume and not pd.isna(volume):
        volume_appezzamento_uri = BASE[f"volume/{volume}"]
        volume_appezzamento_volume_uri = BASE["volume"]

        triples.append((appezzamento_uri, CRM["P1_is_identified_by"], volume_appezzamento_uri))
        triples.append((volume_appezzamento_uri, RDFS["label"], Literal(volume, datatype=XSD.string)))

        triples.append((volume_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((volume_appezzamento_uri, CRM["P2_has_type"], volume_appezzamento_volume_uri))
        triples.append((volume_appezzamento_volume_uri, RDFS["label"], Literal("volume", datatype=XSD.string)))
        triples.append((volume_appezzamento_volume_uri, CRM["P3_has_note"], Literal("volume: for each plot, the number of the register of the series: Firenze, tavole indicative.", datatype=XSD.string)))


    # Debugging: print the values

    # Process sup_bqf
    if not pd.isna(sup_bqf):
        measure_unit_appezzamento_bqf_uri = BASE["braccia_quadrate_fiorentine"]
        dimension_bqf_appezzamento_uri = BASE[f"dimension_bqf/{sup_bqf}"]

        triples.append((appezzamento_uri, CRM["P43_has_dimension"], dimension_bqf_appezzamento_uri))
        triples.append((dimension_bqf_appezzamento_uri, RDFS["label"], Literal(sup_bqf, datatype=XSD.string)))

        triples.append((dimension_bqf_appezzamento_uri, CRM["P2_has_type"], CRM["E54_Dimension"]))
        triples.append((dimension_bqf_appezzamento_uri, CRM["P91_has_unit"], measure_unit_appezzamento_bqf_uri))
        triples.append((dimension_bqf_appezzamento_uri, CRM["P40i_was_observed_in"], measurements_appezzamento_uri))

        triples.append((measure_unit_appezzamento_bqf_uri, CRM["P2_has_type"], CRM["E58_Measurement_Unit"]))
        triples.append((measure_unit_appezzamento_bqf_uri, RDFS["label"], Literal("sup_bqf", datatype=XSD.string)))
        triples.append((measure_unit_appezzamento_bqf_uri, CRM["P3_has_note"], Literal(
            "sup_bqf: surface area in Florentine square arms. Expresses the value of the surface area of the polygon plot in Florentine square arms.", datatype=XSD.string)))

    # Process sup_mq
    if not pd.isna(sup_mq):
        measure_unit_appezzamento_mq_uri = BASE["metri_quadrati"]
        dimension_mq_appezzamento_uri = BASE[f"dimension_mq/{sup_mq}"]

        triples.append((appezzamento_uri, CRM["P43_has_dimension"], dimension_mq_appezzamento_uri))
        triples.append((dimension_mq_appezzamento_uri, RDFS["label"], Literal(sup_mq, datatype=XSD.string)))

        triples.append((dimension_mq_appezzamento_uri, CRM["P2_has_type"], CRM["E54_Dimension"]))
        triples.append((dimension_mq_appezzamento_uri, CRM["P91_has_unit"], measure_unit_appezzamento_mq_uri))
        triples.append((dimension_mq_appezzamento_uri, CRM["P40i_was_observed_in"], measurements_appezzamento_uri))

        triples.append((measure_unit_appezzamento_mq_uri, CRM["P2_has_type"], CRM["E58_Measurement_Unit"]))
        triples.append((measure_unit_appezzamento_mq_uri, RDFS["label"], Literal("sup_mq", datatype=XSD.string)))
        triples.append((measure_unit_appezzamento_mq_uri, CRM["P3_has_note"], Literal(
            "sup_mq: surface area in square meters. Expresses the value of the surface area of the polygon plot in square meters.", datatype=XSD.string)))
        
    if toponomastica and not pd.isna(toponomastica):
        toponomastica_value = sub_space_pattern.sub('_', str(toponomastica).strip().replace("'", "_"))
        toponomast_appezzamento_uri = BASE[f"toponomastica/{toponomastica_value}"]
        toponomast_appezzamento_top_uri = BASE["toponomastica"]

        triples.append((place_appezzamento_uri, CRM["P1_is_identified_by"], toponomast_appezzamento_uri))
        triples.append((toponomast_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((toponomast_appezzamento_uri, RDFS["label"], Literal(toponomastica, datatype=XSD.string)))
        triples.append((toponomast_appezzamento_uri, CRM["P2_has_type"], toponomast_appezzamento_top_uri))
        triples.append((toponomast_appezzamento_top_uri, RDFS["label"], Literal("toponomastica", datatype=XSD.string)))
        triples.append((toponomast_appezzamento_top_uri, CRM["P3_has_note"], Literal("toponomastica: toponymic reference of the parcel.", datatype=XSD.string)))

    if num_civico and not pd.isna(num_civico):
        num_civico_value = sub_space_pattern.sub('_', str(num_civico).strip())
        num_civico_appezzamento_uri = BASE[f"num_civico/{num_civico_value}"]
        num_civico_appezzamento_nc_uri = BASE["num_civico"]

        triples.append((place_appezzamento_uri, CRM["P1_is_identified_by"], num_civico_appezzamento_uri))
        triples.append((num_civico_appezzamento_uri, CRM["P2_has_type"], CRM["E42_Identifier"]))
        triples.append((num_civico_appezzamento_uri, RDFS["label"], Literal(num_civico, datatype=XSD.string)))
        triples.append((num_civico_appezzamento_uri, CRM["P2_has_type"], num_civico_appezzamento_nc_uri))
        triples.append((num_civico_appezzamento_nc_uri, RDFS["label"], Literal("num_civico", datatype=XSD.string)))
        triples.append((num_civico_appezzamento_nc_uri, CRM["P3_has_note"], Literal("num_civico: reference to the civic numbering of the parcel.", datatype=XSD.string)))

    if ente and not pd.isna(ente):
        ente_slim = sub_non_alnum_pattern.sub('', str(ente))
        ente_slimm = sub_space_pattern.sub('_', ente_slim.strip())
        
        ente_ente_uri = BASE["ente"]

        group_uri = BASE[f"group/{ente_slimm}"]

        
        triples.append((group_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((group_uri, CRM["P2_has_type"], ente_ente_uri))
        triples.append((ente_ente_uri, RDFS["label"], Literal("ente", datatype=XSD.string)))
        triples.append((ente_ente_uri, CRM["P3_has_note"], Literal("ente: name of the public, civil or religious owner.", datatype=XSD.string)))
        triples.append((group_uri, RDFS["label"], Literal(ente, datatype=XSD.string)))

        triples.append((group_uri, CRM["P2_has_type"], CRM["E74_Group"]))
        triples.append((group_uri, CRM["P22i_acquired_title_through"], acquisition_appezzamento_uri))

    if nome and not pd.isna(nome) and cognome and not pd.isna(cognome):
        nome_value = sub_space_pattern.sub('_', str(nome).strip())
        nome_uri = BASE[f"nome/{nome_value}"]
        nome_nome_uri = BASE["nome"]

        cognome_value = sub_space_pattern.sub('_', str(cognome).strip())
        cognome_uri = BASE[f"cognome/{cognome_value}"]
        cognome_cogn_uri = BASE["cognome"]

        person_uri = BASE[f"person/{nome_value}_{cognome_value}"]

        triples.append((person_uri, CRM["P1_is_identified_by"], nome_uri))
        triples.append((nome_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((nome_uri, RDFS["label"], Literal(nome, datatype=XSD.string)))
        triples.append((nome_uri, CRM["P2_has_type"], nome_nome_uri))
        triples.append((nome_nome_uri, RDFS["label"], Literal("nome", datatype=XSD.string)))
        triples.append((nome_nome_uri, CRM["P3_has_note"], Literal("nome: owner's first name.", datatype=XSD.string)))

        triples.append((person_uri, CRM["P1_is_identified_by"], cognome_uri))
        triples.append((cognome_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((cognome_uri, RDFS["label"], Literal(cognome, datatype=XSD.string)))
        triples.append((cognome_uri, CRM["P2_has_type"], cognome_cogn_uri))
        triples.append((cognome_cogn_uri, RDFS["label"], Literal("cognome", datatype=XSD.string)))
        triples.append((cognome_cogn_uri, CRM["P3_has_note"], Literal("cognome: owner's family name.", datatype=XSD.string)))

        triples.append((person_uri, CRM["P2_has_type"], CRM["E21_Person"]))
        triples.append((person_uri, CRM["P22i_acquired_title_through"], acquisition_appezzamento_uri))
        label = f"{nome} {cognome}"
        triples.append((person_uri, RDFS["label"], Literal(label, datatype=XSD.string)))

    if patronimico and not pd.isna(patronimico):
        patronimico_value = sub_space_pattern.sub('_', str(patronimico).strip())
        patronimico_uri = BASE[f"patronimico/{patronimico_value}"]
        patronimico_patr_uri = BASE["patronimico"]

        triples.append((person_uri, CRM["P1_is_identified_by"], patronimico_uri))
        triples.append((patronimico_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((patronimico_uri, RDFS["label"], Literal(patronimico, datatype=XSD.string)))
        triples.append((patronimico_uri, CRM["P2_has_type"], patronimico_patr_uri))
        triples.append((patronimico_patr_uri, RDFS["label"], Literal("patronimico", datatype=XSD.string)))
        triples.append((patronimico_patr_uri, CRM["P3_has_note"], Literal("patronimico: patronymic of the owner.", datatype=XSD.string)))

    if moglie_di and not pd.isna(moglie_di):
        moglie_di_value = sub_space_pattern.sub('_', str(moglie_di).strip())
        moglie_di_uri = BASE[f"moglie_di/{moglie_di_value}"]
        moglie_di_md_uri = BASE["moglie_di"]

        triples.append((person_uri, CRM["P1_is_identified_by"], moglie_di_uri))
        triples.append((moglie_di_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((moglie_di_uri, RDFS["label"], Literal(moglie_di, datatype=XSD.string)))
        triples.append((moglie_di_uri, CRM["P2_has_type"], moglie_di_md_uri))
        triples.append((moglie_di_md_uri, RDFS["label"], Literal("moglie_di", datatype=XSD.string)))
        triples.append((moglie_di_md_uri, CRM["P3_has_note"], Literal("moglie_di: first name or full name of the owner's husband.", datatype=XSD.string)))

    if titolo and not pd.isna(titolo):
        titolo_value = sub_space_pattern.sub('_', str(titolo).strip())
        titolo_uri = BASE[f"titolo/{titolo_value}"]
        titolo_tit_uri = BASE["titolo"]

        triples.append((person_uri, CRM["P1_is_identified_by"], titolo_uri))
        triples.append((titolo_uri, CRM["P2_has_type"], CRM["E41_Appellation"]))
        triples.append((titolo_uri, RDFS["label"], Literal(titolo, datatype=XSD.string)))
        triples.append((titolo_uri, CRM["P2_has_type"], titolo_tit_uri))
        triples.append((titolo_tit_uri, RDFS["label"], Literal("titolo", datatype=XSD.string)))
        triples.append((titolo_tit_uri, CRM["P3_has_note"], Literal("titolo: owner's title.", datatype=XSD.string)))



    g += triples

print("Tempo loop:", time.time() - loop_start_time)


output_directory = os.path.dirname(csv_file_path)

output_file = os.path.join(output_directory, "output_data.nt")

start_serialization_time = time.time()
g.serialize(destination=output_file, format="nt")
print(f"RDF saved in NT format: {output_file}")
print(f"Serialization time: {time.time() - start_serialization_time} seconds")


import subprocess

# Define the prefixes
prefixes = {
    "crm": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
}

# Construct the rapper command with prefixes
rapper_command = [
    "rapper",
    "-i", "ntriples",
    "-o", "turtle"
]

# Add the -f flags with prefixes
for prefix, uri in prefixes.items():
    xmlns_feature = f'xmlns:{prefix}="{uri}"'
    rapper_command.extend(["-f", xmlns_feature])

# Specify the input and output files
input_nt_file = output_file
output_ttl_file = os.path.join(output_directory, "output_data_converted_final.ttl")

# Complete the command with input file
rapper_command.append(input_nt_file)

# Open the output file to write the converted Turtle data
with open(output_ttl_file, 'w', encoding='utf-8') as outfile:
    # Run the rapper command and redirect output to the file
    subprocess.run(rapper_command, stdout=outfile)

GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Print in green
print(f"{GREEN}Conversion completed: {input_nt_file} -> {output_ttl_file}{RESET}")

# Print in blue
print(f"{BLUE}Total time: {time.time() - total_time:.2f} seconds{RESET}")


