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

file1 = "C:\\Users\\erica\\Desktop\\METAPOLIS\\proprietari_update\\merged_data_modified.csv"
file2 = "C:\\Users\\erica\\Desktop\\METAPOLIS\\proprietari_update\\parcellizzazione_fondiaria.csv"

df1 = pd.read_csv(file1, delimiter=';')
df2 = pd.read_csv(file2)

df1.columns = df1.columns.str.strip().str.lower()
df2.columns = df2.columns.str.strip().str.lower()

print("Columns in df1:", df1.columns)
print("Columns in df2:", df2.columns)


columns_to_compare = {
    "foglio": "foglio",
    "sezione": "sezione",
    "toponomastica": "toponomast",
    "numero_civico": "num_civico"
}

df1['first_number_appezzamento'] = df1['first_number_appezzamento'].astype(str)
df2['appezzamen'] = df2['appezzamen'].astype(str)


merged_df = pd.merge(
    df1,
    df2,
    left_on="first_number_appezzamento",
    right_on="appezzamen",
    how="outer",  # To include all rows for analysis
    indicator=True
)

differences = []
for col1, col2 in columns_to_compare.items():
    merged_df[f"match_{col1}"] = merged_df[col1] == merged_df[col2]
    diff_rows = merged_df[~merged_df[f"match_{col1}"] & merged_df[f"{col1}"].notna() & merged_df[f"{col2}"].notna()]
    if not diff_rows.empty:
        differences.append((col1, col2, diff_rows))


merged_df.to_csv("merged_results.csv", index=False)

with open("differences_summary.txt", "w") as f:
    for col1, col2, diff_rows in differences:
        f.write(f"Differences in columns {col1} and {col2}:\n")
        f.write(diff_rows.to_string())
        f.write("\n\n")

print("Analysis completed. Results saved to 'merged_results.csv' and 'differences_summary.txt'.")
