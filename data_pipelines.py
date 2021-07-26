import zipfile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress
import json
from json import dumps

def drug_classification(drugs_data, publication_data):
    finaldf = []
    temp = drugs_data['drug'].apply(lambda x: x.strip()).to_list() # We select the name of all the drugs in the Dataframe
    for drug in temp:
        l = publication_data["title"].str.contains(drug).to_list()  # We select the publications with the drug mentionned in it
        lt = list(compress(range(len(l)), l))
        row_pubmed = []
        row_journal = []
        for s in lt:
            row = []
            row.append(drug)
            row.append(drugs_data[drugs_data["drug"] == drug]["atccode"].iloc[0])
            row.append(publication_data["publication_type"].loc[s])
            row.append(publication_data["id"].loc[s])
            row.append(publication_data["date"].loc[s])
            row_pubmed.append(row)
            if publication_data["journal"].loc[s] is not None: # We check that we don't have nan values in journal
                row2 = []
                row2.append(drug)
                row2.append(drugs_data[drugs_data["drug"] == drug]["atccode"].iloc[0])
                row2.append("Journal")
                row2.append(publication_data["journal"].loc[s])
                row2.append(publication_data["date"].loc[s])
                row_journal.append(row2)
                rowf = row_pubmed + row_journal
        finaldf = finaldf + rowf
    return finaldf


def df_to_json(df,drugs_data):
    json_dict = {}
    json_dict['Drug_classification'] = []
    for grp, grp_data in df.groupby('Drug_name'):
        grp_dict = {}
        grp_dict['Drug_name'] = grp
        grp_dict['Drug_atccode'] = drugs_data[drugs_data["drug"] == grp]["atccode"].iloc[0]
        grp_dict['Publications'] = []
        for p, p_data in grp_data.groupby('Type'):
            p_data = p_data.drop(['Drug_name', 'Drug_atccode'], axis=1).set_index('Type')
            for d in p_data.to_dict(orient='records'):
                grp_dict['Publications'].append({'Type': p, 'Date': d['date'].__str__(), 'Source_ID': d['Source_ID']})
        json_dict['Drug_classification'].append(grp_dict)
    json_out = dumps(json_dict)
    parsed = json.loads(json_out)
    with open('drug_classification.json', 'w') as f:
        json.dump(parsed, f)

        