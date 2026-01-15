import pandas as pd
import numpy as np

df = pd.read_csv('Measurements 4.csv')
opcion = int(input("1.- Prueba de continuidad\n2.- Prueba de Aislamiento\n"))


umbral = 1000
res = "Primary Measurement"
no = "Notas"
si = "Remark"

num2 = pd.to_numeric(df[res], errors="coerce")

df[no] = np.where(num2 > 2, df[no], "X")
df[si] = np.where(num2 > 2, df[si], " ")

df[si] = np.where(num2 < 2, df[si], "X ")
df[no] = np.where(num2 < 2, df[no], " ")


if opcion == 1:

    prueba = ['Prueba de continuidad']
    df = df[df['Test Function'].isin(prueba)].copy()
    rows = df.to_dict("records")
    salida = []
    i = 0


    res = "Primary Measurement"
    no = "Notas"
    si = "Remark"

    num2 = (
    df[res]
    .astype(str)
    .str.extract(r'([-+]?\d*\.?\d+)')[0]
    .astype(float))
    
    df[no] = np.where(num2 > 2, "X", "")
    df[si] = np.where(num2 <= 2, "X", "")


    while i < len(rows):
        a = rows[i]

        if i + 1 < len(rows) and a["Configuración"] == rows[i+1]["Configuración"]:
            b = rows[i+1]
            out = {**{f"{k}_B": v for k, v in a.items()},
                **{f"{k}_A": v for k, v in b.items()}}
            i += 2
        else:

            out = {f"{k}_B": v for k, v in a.items()}
            out.update({f"{k}_A": np.nan for k in a.keys()})
            i += 1

        salida.append(out)

    df_final = pd.DataFrame(salida)

    contexto = ["Configuración", "Test Function", "Level A", "Level C"]
    for c in contexto:
        df_final[f"{c}_A"] = df_final[f"{c}_A"].fillna(df_final[f"{c}_B"])


    desired_columns = [
        "Configuración_A","Test Function_A","Level A_A","Level C_A",
        "Primary Measurement_A","Primary Measurement_B", "Remark_A", "Notas_A"
    ]
    df = df_final[desired_columns].copy()




    df = df.reset_index(drop=True)

    col_circ = "Level C_A"
    col_cfg  = "Configuración_A"

    cargas = []
    circuito_prev = None
    cfg_prev = None
    cfg_block = 0

    for j in range(len(df)):
        circuito = str(df.at[j, col_circ]).strip()
        cfg = str(df.at[j, col_cfg]).strip()

        if j == 0 or circuito != circuito_prev:
            cfg_block = 0
            cfg_prev = None

        if cfg_prev is None or cfg != cfg_prev:
            cfg_block += 1

        carga = ((cfg_block - 1) // 3) + 1
        cargas.append(carga)

        circuito_prev = circuito
        cfg_prev = cfg

    df["Carga"] = cargas


    df = df.rename(columns={
        "Primary Measurement_A": "Resistencia (+)", 
        "Primary Measurement_B": "Resistencia (-)",
        "Level C_A": "N° Circuito",
        "Level A_A": "Alimentador",
        "Test Function_A": "Prueba   ",
        "Configuración_A": "Configuración", "Remark_A": " SI ",
          "Notas_A": " NO "})
    
    alimentador = "Alimentador"
    cir = "N° Circuito"

    num = pd.to_numeric(df[alimentador], errors="coerce")
    df[alimentador] = np.where(num > umbral, df[alimentador], "falso")
    df[cir] = np.where(num > umbral, "Al.", df[cir])


    desired_columns = ["N° Circuito","Alimentador", "Carga", "Configuración",
    "Resistencia (+)","Resistencia (-)", " SI ", " NO "]
    df = df[desired_columns].copy()
    df.to_csv("Resultado_continuidad.csv", index=False)

else:
    prueba = ['Prueba de aislamiento']
    df = df[df['Test Function'].isin(prueba)].copy()


    res = "Primary Measurement"
    no = "Notas"
    si = "Remark"
    
    num2 = (
    df[res]
    .astype(str)
    .str.extract(r'([-+]?\d*\.?\d+)')[0]
    .astype(float))


    df[no] = np.where(num2 < 0.5, "X", "")
    df[si] = np.where(num2 >= 0.5, "X", "")

    df = df.rename(columns={"Primary Measurement": "Resistencia", "Level A": "Alimentador", "Remark": " SI ",
          "Notas": " NO "})
    desired_columns = ["Alimentador", "Configuración", "Resistencia", " SI ", " NO "]
    df = df[desired_columns].copy()

    alimentador = "Alimentador"
    num = pd.to_numeric(df[alimentador], errors="coerce")
    df[alimentador] = np.where(num > umbral, df[alimentador], "falso")
    df.to_csv("Resultado_aislamiento.csv", index=False)




print(df)

