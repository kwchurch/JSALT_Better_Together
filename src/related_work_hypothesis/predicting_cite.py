import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import ast


def es_lista_valida(cadena):
    try:
        lista_convertida = ast.literal_eval(cadena)
        return isinstance(lista_convertida, list)
    except (ValueError, SyntaxError):
        return False


FILEPATH = os.path.dirname("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/predicting_vectors/")
raw_dirs = set([d for d in os.listdir(FILEPATH)])

# Lista para almacenar los DataFrames de cada archivo

x,z = [],[]

for archivo in raw_dirs:
    with open(FILEPATH+"/"+archivo, "r") as file:
        flag = 0
        for line in file:
            if line.find("V") == -1:
                line = line.replace("\n","")
                line = line.replace("'","")
                z.append(ast.literal_eval(line.split("\t")[1]))
                x.append(ast.literal_eval(line.split("\t")[2]))
                #y.append(ast.literal_eval(line.split("\t")[3]))



# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, Z_train, Z_test = train_test_split(x, z, test_size=0.2, random_state=42)


# Crear y entrenar el modelo de regresión logística
logistic_model = LogisticRegression()
logistic_model.fit(X_train, Z_train)

# Realizar predicciones en el conjunto de prueba
Z_pred = logistic_model.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy = accuracy_score(Z_test, Z_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy * 100))

'''
    df = pd.read_csv(FILEPATH+"/"+archivo, sep='\t')
    dataframes.append(df)

df = pd.concat(dataframes)


print(df.head())

print(df.dtypes)

# Supongamos que 'df' es tu DataFrame y 'mi_columna' es la columna que deseas convertir a arrays NumPy
df['V_nrw'] = df['V_nrw'].apply(np.array)


print(df.dtypes)
# Filtrar filas con valores no válidos en las columnas 'V_rw', 'V_nrw' y 'V_prone'

for index, row in df.iterrows():
    print(type(row['V_nrw']))






# Convertir las columnas a valores numéricos
df_numeric['V_rw'] = df_numeric['V_rw'].astype(float)
df_numeric['V_nrw'] = df_numeric['V_nrw'].astype(float)
df_numeric['V_prone'] = df_numeric['V_prone'].astype(float)

# Convertir las listas de listas a matrices numpy después de filtrar y convertir los datos
X = np.array(df_numeric[['V_rw', 'V_nrw']].values.tolist())
y = np.array(df_numeric['V_prone'])

# Separamos los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creamos el modelo de regresión logística
model = LogisticRegression()

# Entrenamos el modelo con los datos de entrenamiento
model.fit(X_train, y_train)

# Realizamos predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Evaluamos la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy * 100))

'''