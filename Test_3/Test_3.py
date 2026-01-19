import pandas as pd
import numpy as np

C_dif = int(input("Ingrese la cantidad de diferenciales: "))
C_cir_global = 1

diferenciales = {}
for d in range(1, C_dif + 1):
    n_c = int(input(f"Circuitos en diferencial {d}: "))
    diferenciales[d] = list(range(C_cir_global, C_cir_global + n_c))
    C_cir_global += n_c

circuito_a_dif = {c: d for d, cs in diferenciales.items() for c in cs}

def dif_de_circuito(c):
    try:
        return circuito_a_dif.get(int(c), None)
    except:
        return None

df = pd.read_csv("test.csv")

mask_pe = df["Configuración"].astype(str).isin(["N-PE", "L-PE"])
df_pe = df[mask_pe].copy()
df = df[~mask_pe].copy()





df["Configuración"] = df["Configuración"].astype(str).str.strip()
df["Level B"] = pd.to_numeric(df["Level B"], errors="coerce")
df["Level C"] = pd.to_numeric(df["Level C"], errors="coerce")
df = df[df["Level B"].notna() & df["Level C"].notna()].copy()

df["_idx"] = np.arange(len(df))

Pruebas_ordenadas = {
    0: ("F", "F", "L-N"),
    1: ("F", "N", "L-N"),
    2: ("N", "F", "L-N"),
    3: ("N", "N", "L-N"),
}

df = df.sort_values(["Level B", "Level C", "_idx"]).copy()
df["_pos"] = df.groupby(["Level B", "Level C"]).cumcount()
df = df[df["_pos"].between(0, 3)].copy()

df["COND_A"] = df["_pos"].map(lambda p: Pruebas_ordenadas[p][0])
df["COND_B"] = df["_pos"].map(lambda p: Pruebas_ordenadas[p][1])
df["CFG_ESPERADA"] = df["_pos"].map(lambda p: Pruebas_ordenadas[p][2])
df["OBS_EXTRA"] = np.where(df["Configuración"] != df["CFG_ESPERADA"], "CFG distinta", "")

out_rows = []

def add_row(cir_A, conductor_A, cir_B, conductor_B, resistencia, obs=""):
    out_rows.append({
        "Circuito_A": str(cir_A),
        "F/N/T": str(conductor_A),
        "Circuito_B": str(cir_B),
        "F/N/T ": str(conductor_B),
        "Resistencia": resistencia if pd.notna(resistencia) else "",
        "SI": "",
        "NO": "",
        "Observación": obs
    })

for _, r in df.iterrows():
    A = int(r["Level B"])
    B = int(r["Level C"])
    add_row(
        A,
        r["COND_A"],
        B,
        r["COND_B"],
        r.get("Primary Measurement", ""),
        obs=r.get("OBS_EXTRA", "")
    )

out = pd.DataFrame(out_rows)

out["_tipo_key"] = (
    out["Circuito_A"].astype(str) + "|" +
    out["F/N/T"].astype(str) + "|" +
    out["Circuito_B"].astype(str) + "|" +
    out["F/N/T "].astype(str)
)
out = out.drop_duplicates(subset=["_tipo_key"], keep="first").drop(columns=["_tipo_key"])

def key_circuito(x):
    s = str(x).strip()
    if s.isdigit():
        return (0, int(s))
    return (1, 10**9)

out["_kA"] = out["Circuito_A"].apply(key_circuito)
out["_kB"] = out["Circuito_B"].apply(key_circuito)
out = out.sort_values(["_kA", "_kB", "F/N/T", "F/N/T "]).drop(columns=["_kA", "_kB"])

res = "Resistencia"
si = "SI"
no = "NO"
cirA = "Circuito_A"
cirB = "Circuito_B"
conf_A = "F/N/T"
conf_B = "F/N/T "
obs = "Observación"
conf = "Configuración"

A_num = pd.to_numeric(out[cirA].astype(str).str.strip(), errors="coerce")
B_num = pd.to_numeric(out[cirB].astype(str).str.strip(), errors="coerce")

dif_A = A_num.map(circuito_a_dif)
dif_B = B_num.map(circuito_a_dif)

mask_mismo_dif_nn = (dif_A == dif_B) & (out[conf_A] == "N") & (out[conf_B] == "N")
out.loc[mask_mismo_dif_nn, res] = "-"
out.loc[mask_mismo_dif_nn, obs] = "Mismo Dif."

num2 = (
    out[res]
    .astype(str)
    .str.extract(r'([-+]?\d*\.?\d+)')[0]
    .astype(float)
)

out[no] = np.where(num2 < 0.5, "X", "")
out[si] = np.where(num2 >= 0.5, "X", "")

out_pe = pd.DataFrame({
    "Circuito_A": df_pe["Level B"].astype(str),
    "F/N/T": "",
    "Circuito_B": df_pe["Level C"].astype(str),
    "F/N/T ": "",
    "Resistencia": df_pe.get("Primary Measurement", ""),
    "SI": "",
    "NO": "",
    "Observación": ""
})



map_otro = {
    "N-PE": "N",
    "L-PE": "F"
}

out_pe[cirA] = df_pe["Level C"].astype(str)
out_pe[conf_A] = df_pe[conf].map(map_otro).fillna("")

out_pe[cirB] = "Barra"
out_pe[conf_B] = "T"


out_pe["_ord"] = pd.to_numeric(out_pe[cirA].astype(str).str.extract(r"(\d+)", expand=False), errors="coerce")
out_pe = out_pe.sort_values(["_ord"]).drop(columns=["_ord"])



dif_A = pd.to_numeric(out_pe[cirA].astype(str).str.strip(), errors="coerce").map(circuito_a_dif)
mask_npe = (out_pe[conf_A] == "N") & (out_pe[conf_B] == "T")
mask_repetido = mask_npe & dif_A.notna() & dif_A.where(mask_npe).duplicated()
out_pe.loc[mask_repetido, obs] = "Mismo Dif."
out_pe.loc[mask_repetido, res] = "-"

out = pd.concat([out, out_pe], ignore_index=True)

num2 = (
    out[res]
    .astype(str)
    .str.extract(r'([-+]?\d*\.?\d+)')[0]
    .astype(float)
)

out[no] = np.where(num2 < 0.5, "X", "")
out[si] = np.where(num2 >= 0.5, "X", "")


out.to_csv("output.csv", index=False)
print("output.csv")
