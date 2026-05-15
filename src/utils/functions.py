import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

def distribucionCategoricas(df, categoricas, relativa=False, mostrar_valores=False):
    num_columnas = len(categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(15, 5 * num_filas))
    axes = axes.flatten() 

    for i, col in enumerate(categoricas):
        ax = axes[i]
        if relativa:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='magma', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            serie = df[col].value_counts()
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='magma', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

def plot_multiple_boxplots(df, columns, dim_matriz_visual = 2):
    num_cols = len(columns)
    num_rows = num_cols // dim_matriz_visual + num_cols % dim_matriz_visual
    fig, axes = plt.subplots(num_rows, dim_matriz_visual, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.boxplot(data=df, x=column, ax=axes[i], palette='magma',)
            axes[i].set_title(column)

    # Ocultar ejes vacíos
    for j in range(i+1, num_rows * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def plot_boxplot_grouped(df, column_to_plot, group_column):
    if df[column_to_plot].dtype in ['int64', 'float64'] and df[group_column].dtype in ['object', 'category']:
        sns.boxplot(data=df, x=group_column, y=column_to_plot, palette='magma',)
        plt.show()