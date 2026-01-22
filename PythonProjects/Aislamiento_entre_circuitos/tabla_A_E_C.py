import pandas as pd
import numpy as np

C_dif = int(input("Ingrese la cantidad de diferenciales: "))
C_cir = 1

df = pd.DataFrame(columns=["Circuito_A", "F/N/T","Circuito_B", "F/N/T ", "Resistencia", "Conforme", "Observación"])


def add_row(df, row_dict):
    df.loc[len(df)] = row_dict
    return df

def mismo_diferencial(c1, c2, diferenciales):
    for d, circuitos in diferenciales.items():
        if c1 in circuitos and c2 in circuitos:
            return True
    return False


diferenciales = {}

for d in range(1, C_dif + 1):
    n_c = int(input((f"Circuitos en diferencial {d}: ")))

    diferenciales[d] = list(range(C_cir, C_cir + n_c))

    C_cir += n_c
C_cir -=1

print (C_dif)
print(C_cir)

print(len(diferenciales))

def cantidad_circuitos(diferenciales, diferencial_id):
    return len(diferenciales.get(diferencial_id, []))

print(cantidad_circuitos(diferenciales,1))




for i in range(1, C_cir + 1):

    for k in range(i+1, C_cir +1):
        df = add_row(df, { "Circuito_A": f"{i}", "F/N/T": "F","Circuito_B": f"{k}","F/N/T ": "F", "Resistencia": "     ",
                               "Conforme": " si [    ]     no [    ] ", "Observación": "                           " })
        
        df = add_row(df, { "Circuito_A": f"{i}", "F/N/T": "F","Circuito_B": f"{k}","F/N/T ": "N", "Resistencia": "     ",
                               "Conforme": " si [    ]     no [    ] ", "Observación": "                           " })
        
        df = add_row(df, { "Circuito_A": f"{i}", "F/N/T": "N","Circuito_B": f"{k}","F/N/T ": "F", "Resistencia": "     ",
                               "Conforme": " si [    ]     no [    ] ", "Observación": "                           " })
        
        if mismo_diferencial(i,k,diferenciales):
            df = add_row(df, { "Circuito_A": f"{i}", "F/N/T": "N","Circuito_B": f"{k}","F/N/T ": "N", "Resistencia": "N/A",
                               "Conforme": "N/A", "Observación": "Mismo diferencial" })
        else:
            df = add_row(df, { "Circuito_A": f"{i}", "F/N/T": "N","Circuito_B": f"{k}","F/N/T ": "N", "Resistencia": "     ",
                               "Conforme": " si [    ]     no [    ] ", "Observación": "                           " })



for i in range(1, C_cir + 1):
    df = add_row(df, { "Circuito_A": f"Barra", "F/N/T": "T","Circuito_B": f"{i}","F/N/T ": "F", "Resistencia": "     ",
                         "Conforme": " si [    ]     no [    ] ", "Observación": "                           " }) 
    
    if mismo_diferencial(i, i-1, diferenciales):
            df = add_row(df, { "Circuito_A": "Barra", "F/N/T": "T","Circuito_B": f"{i}","F/N/T ": "N", "Resistencia": " N/A ",
                                "Conforme": "N/A", "Observación": "Mismo diferencial" })    
    else:
            df = add_row(df, { "Circuito_A": "Barra", "F/N/T": "T","Circuito_B": f"{i}","F/N/T ": "N", "Resistencia": "     ",
                                "Conforme": " si [    ]     no [    ] ", "Observación": "                           " })  

        
df.to_csv("Tablas_vacias/Tabla_A_E_C.csv", index=False)



