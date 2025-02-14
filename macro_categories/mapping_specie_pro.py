# -*- coding: utf-8 -*-
# Copyright (c) 2024,
# Erica Andreose
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
import numpy as np
import csv

df = pd.read_csv('specie_pro_type.csv')


def assign_macro_category(specie_pro):
    if pd.isnull(specie_pro):
        return 'spazio aperto'

    specie_pro = specie_pro.lower()

    # Fabbricato Urbano
    fabbricato_urbano_keywords = [
        "casa", "palazzo", "stabile", "magazzino", "fabbricato", "rimessa", "villa", 
        "casamento", "stanza", "stanzone", "quartiere", "casa colonica", "stabile", "appartamento", 
        "pian terreno", "mezzanino", "palazzetto", "locale", "palazzina", "ingresso", "androne", "corridoio", "andito", "passare", "corridore", "vestibolo",
        "fondo", "cantina", "fienile", "granaio", "rondò", "uccelliera", "casino", "stufa", "grotta", "caffeaus", "annesso", "guindolo", "capanna",
        "edificio", "loggia", "terrazza", "torre", "polveriera", "porta", "castello", "gabellino", "mura", "arsenale",
        "fortezza", "torrino", "stanze", "edifici", "cucina", "sotterraneo", "26 e 3  piano", "stufe", "parte di 1t 2c e 3\ piano",
        "fondi", "stalletta", "stanzino", "stanzoni", "siti", "scala a comune", "pollaio", "magazzini", "sito coperto", "villino",
        "sala di artifizio", "casetta"
    ]
    
    # Spazio Religioso
    spazio_religioso_keywords = [
        "chiesa", "oratorio", "compagnia", "sagrestia", "convento", "cappella", "monastero", 
        "battistero", "santuario", "luogo religioso", "chiesa e casa", "casa e chiesa", "campanile", "tabernacolo",
        "canonica", "seminario", "cimitero", "campo santo", "stanza mortuaria", "camposanto"
    ]
    
    # Spazio Aperto Verde
    spazio_aperto_verde_keywords = [
        "orto", "giardino", "bosco", "prato", "albereto", "parco", "fattoria", "vivaio", 
        "agricoltura", "campagna", "seminativo", "piantagione", "pascolo", "lavorativo", "terreno",
        "sodo", "pastura", "canneto", "alberata", "alberato", "albereta", "ortivo", "pioppato", "fruttato", "orti",
        "giardinetto", "luoghi per dianjaje", "massechito", "luoghi comodi", "lecceta", "boschetto", "prativo", "nicchia prativa",
        "plantarnari", "pratello", "giardino storico", "sodi", "piantonaia", "labirinto", "sodivo con gelsi", "rese di detta strada", "parterre",
        "luogo di delizia"
    ]
    
    # Spazio Aperto
    spazio_aperto_keywords = [
        "corte", "piazza", "strada", "passaggio", "piazzale", "vicolo", 
        "spazio aperto", "aia", "portico", "cortile", "anfiteatro", "gioco del pallone", "giuoco del pallone",
        "labirinto", "luogo di delizia", "parterre", "bagnaia", "passo a comune", "stradone", "passeggio", "viale", "sodi",
        "orticello", "spalla di Arno", "viottolo", "luogo d'adunanza", "viottole", "piazzetta", "luogo del rastrello", "chiasso a comune",
        "viottola", "stradella", "spiazzo", "viali", "metropolitana", "strada", "corte comune", "corte comune", "aia", "corte", "passo a comune e corte",
        "piazza", "piazza e trogoli", "concimaia", "piazza della cera", "luogo del rastrello", "spalla di arno"
    ]
    
    # Acque
    acque_keywords = [
        "vasca", "fontana", "laguna", "gora", "canale", "fiume", "piscina", "conserva", "acqua", "pozzo", "bagno", "lavatoio", "conserva d'acqua", "serbatoio",
        "corso d'acqua", "ghiacciaia aperta", "ghiacciaia chiusa", "lavatoi", "bindolo", "fonte", "bagnaia", "ghiacciaia e corte", "ghiacciaia", "bagni e corte"
    ]
    
    # Attività
    attività_keywords = [
        "laboratorio", "officina", "falegnameria", "forno", "mulino", "tintoria", "lavatoio", 
        "attività", "artigianale", "bottega", "macelleria", "fabbro", "panificio", "locanda", 
        "trattoria", "ristorante", "banco", "madiella", "stalla", "scuderia", "ammazzatoio", "porchereccia",
        "concimaia", "luogo di comodo", "stanze del peso pubblico", "fornace", "calcinaia", "concia", "molino", "mulino",
        "studio", "fabbrica", "botteghe", "scuderie", "bottega e corte", "spezieria e corte", "bottega e corte", "stalla e corte", "scuderie e corte",
        "fornace e corte", "conciaio e corte", "bottega, corte e fabbrica", "banco e corte"
    ]
    
    # Servizi
    servizi_keywords = [
        "scuola", "ospedale", "servizio", "ufficio", "biblioteca", "carcere", "amministrazione", 
        "teatro", "tribunale", "polizia", "guardia", "magistratura", "commissariato", "servizi", "ospizio", "infermeria", "partoria", "farmacia",
        "spezieria", "liceo", "conservatorio", "libreria", "gabinetto", "azienda del bollo", "azienda del registro", "scrittoio", "caserma", "corpo di guardia",
        "carcere", "carceri", "biliardo", "spedale", "scuole", "pallottolaio", "teatro e corte", "spedale e corte", "liceo e corte", "concia e corte", "corte e bottega",
        "caserma e corte", "scuola e corte", "scuole e corte", "guardia e corte", "carceri e corte"
    ]
    
    # Controlla la presenza di keyword per ogni macro categoria
    if any(keyword in specie_pro for keyword in fabbricato_urbano_keywords):
        return 'Urban buildings'
    elif any(keyword in specie_pro for keyword in spazio_religioso_keywords):
        return 'Religious buildings'
    elif any(keyword in specie_pro for keyword in spazio_aperto_verde_keywords):
        return 'Open spaces (green)'
    elif any(keyword in specie_pro for keyword in spazio_aperto_keywords):
        return 'Open spaces'
    elif any(keyword in specie_pro for keyword in acque_keywords):
        return 'Waterways'
    elif any(keyword in specie_pro for keyword in attività_keywords):
        return 'Commercial'
    elif any(keyword in specie_pro for keyword in servizi_keywords):
        return 'Services'
    else:
        return 'nc'


df['macro_categoria'] = df['specie_pro'].apply(assign_macro_category)


df.to_csv('macro.csv', index=False, quoting=csv.QUOTE_ALL, quotechar='"')


df_nc = df[df['macro_categoria'] == 'nc']


df_nc.to_csv('solo_nc.csv', index=False, quoting=csv.QUOTE_ALL, quotechar='"')

