import pandas as pd

def obtenerCardinalidad(df):
    """
    Calcula la cardinalidad y tipificación de las columnas de un DataFrame.
    
    Parámetros:
        df (pd.DataFrame): DataFrame de entrada a analizar.
    
    Retorna:
        pd.DataFrame: DataFrame 'df_cardinalidades' con Card, Card_pct y Tipo.
    """
    df_cardinalidades = pd.DataFrame([
        df.nunique(),
        df.nunique() / len(df) * 100,
        df.dtypes
    ]).T.rename(columns={
        0: "Card",
        1: "Card_pct",
        2: "Tipo"
    })
    
    df_cardinalidades["Card"] = df_cardinalidades["Card"].astype(int)
    df_cardinalidades["Card_pct"] = df_cardinalidades["Card_pct"].astype(float).round(2)
    
    return df_cardinalidades

def clasificarVariables(df_original):
    """
    Clasifica las variables de un DataFrame según su cardinalidad.
    
    Parámetros:
        df_original (pd.DataFrame): DataFrame de entrada a analizar.
    
    Retorna:
        pd.DataFrame: DataFrame con la clasificación de cada variable.
    """
    df = obtenerCardinalidad(df_original)
    
    df["Clasificada_como"] = "Categorica"
    df.loc[df["Card"] == 2, "Clasificada_como"] = "Binaria"
    df.loc[df["Card"] > 10, "Clasificada_como"] = "Numerica Discreta"
    df.loc[df["Card_pct"] > 30, "Clasificada_como"] = "Numerica Continua"
    
    return df