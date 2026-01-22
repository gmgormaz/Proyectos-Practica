import pandas as pd
import numpy as np


def add_row(df, row_dict):
    df.loc[len(df)] = row_dict
    return df


choice = int(input("1.- Prueba de continuidad\n2.-Prueba de aislamineto\n"))


if choice == 1:

    df = pd.DataFrame(columns=["Circuito", "Carga","Configuración", "Resistencia (+)", "Resistencia (-)", "Conformidad", "Observación"])
    df.to_csv("output.csv", index=False)

    al = int(input("N° Alimentadores: "))
    cir = int(input("N° Circuitos: "))

    for i in range(0,cir):

        cargas = int(input(f"Cargas circuito {i+1}: "))

        for k in range(0,cargas):

            df = add_row(df, { "Circuito": f"N°{i +1}", "Carga": f"{k+1}","Configuración": " N-PE", "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
            df = add_row(df, {"Circuito": f"N°{i +1}", "Carga": f"{k+1}","Configuración": " L-PE",  "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
            df = add_row(df, {"Circuito": f"N°{i +1}", "Carga": f"{k+1}", "Configuración": " L-N",  "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
       
       
        df = add_row(df, {"Configuración": " ", "Circuito": " ", "Carga": " ", "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                                "Conformidad": " ", "Observación": "                        " })
   


    df = add_row(df, {"Configuración": " ", "Circuito": " ", "Carga": " ", "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                                "Conformidad": " ", "Observación": "                        " })
    df = add_row(df, {"Circuito": "Alimentador", "Carga": "Configuración", "Configuración": "Resistencia (+)", "Resistencia (+)": "  Resistencia (-) ", 
                      "Resistencia (-)": "Conformidad"})



    for i in range(0,al):

        df = add_row(df, {"Configuración": "     ", "Alimentador": "N-PE", "Resistencia (+)": "     ", "Resistencia (-)": " si [    ]     no [    ] ",
                               "Conformidad": " ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": "    ", "Alimentador": " N-PE", "Resistencia (+)": "     ", "Resistencia (-)": " si [    ]     no [    ] ",
                               "Conformidad": " ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": "    ", "Alimentador": " L-N", "Resistencia (+)": "     ", "Resistencia (-)": " si [    ]     no [    ] ",
                               "Conformidad": " ", "Observación": "                           " })
        
        df = add_row(df, {"Configuración": "  ", "Alimentador": "      ", "Resistencia (+)": "     ", "Resistencia (-)": "     ",
                               "Conformidad": " ", "Observación": "                           " })
        

    df.to_csv("output.csv", index=False)

else:

    df = pd.DataFrame(columns=["Configuración", "Circuito","Resistencia", "Conformidad", "Observación"])
    df.to_csv("output.csv", index=False)


    al = int(input("N° Alimentadores: "))
    cir = int(input("N° Circuitos: "))

    for i in range(0, cir):
        df = add_row(df, {"Configuración": " N-PE", "Circuito": f"N°{i +1}", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": " L-PE", "Circuito": f"N°{i +1}", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": " L-N", "Circuito": f"N°{i +1}", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
        
        df = add_row(df, {"Configuración": " ", "Circuito": " ", "Resistencia": "     ",
                               "Conformidad": " ", "Observación": "                           " })       


    df = add_row(df, {"Configuración": "Configuración","Circuito": "Alimentador", "Resistencia": "Resistencia",
                       "Conformidad": "Conformidad","Observación": "Observación" })
    
    for i in range(0, al):
        df = add_row(df, {"Configuración": " N-PE", "Circuito": " ", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": " L-PE", "Circuito": " ", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
            
        df = add_row(df, {"Configuración": " L-N", "Circuito": " ", "Resistencia": "     ",
                               "Conformidad": " si [    ]     no [    ] ", "Observación": "                           " })
        
        df = add_row(df, {"Configuración": " ", "Circuito": " ", "Resistencia": "     ",
                               "Conformidad": "  ", "Observación": "                           " })
    df.to_csv("Tablas_vacias/Tabla_impresion.csv", index=False)

