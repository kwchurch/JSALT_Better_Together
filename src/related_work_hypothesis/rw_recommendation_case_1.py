from transformers import AutoTokenizer, AutoModel
import argparse
import pandas as pd
import numpy as np
from util import get_cosine, get_centroid
import matplotlib.pyplot as plt
from util_prone import directory_to_config
from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from tensorflow.keras.preprocessing.sequence import pad_sequences


tokenizer = AutoTokenizer.from_pretrained('allenai/specter2')
model = AutoModel.from_pretrained('allenai/specter2')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--ref", help="References File", default='../related_work_hypothesis/references_files/all_ref.txt')
    parser.add_argument("-w", "--related", help="Related Work References File", default='../related_work_hypothesis/references_files/related_work_ref.txt')
    parser.add_argument("-c", "--compare", help="Compare file",
                        default='../related_work_hypothesis/references_files/db_test.txt')
    args = parser.parse_args()
    return args


def get_vector_prone(idx, model):
    configs = directory_to_config(model)
    use_map = configs['map']
    use_emb = configs['embedding']
    try:
        paper_emb = use_emb[use_map[int(idx)]]
    except:
        print(f'failed with {int(idx)}')
    return np.array(paper_emb)


def get_vector_hf(title):
    inputs = tokenizer(title, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    embeddings = result.last_hidden_state[:, 0, :]
    return embeddings.detach().numpy().reshape(-1).astype(np.float32)


def clustering_kmeans(arr,n_clusters):
    vectores = np.array(arr)
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(vectores)
    etiquetas = kmeans.labels_
    centroides = kmeans.cluster_centers_
    colores = ['red', 'green', 'blue','yellow']
    vector_colores = [colores[label] for label in etiquetas]
    plt.subplot(121)
    plt.scatter(vectores[:, 0], vectores[:, 1], c=vector_colores)
    plt.scatter(centroides[:, 0], centroides[:, 1], marker='X', color='black')
    plt.savefig('cluster_cites.png')
    contadores = np.bincount(etiquetas)
    grupo_mayor = np.argmax(contadores)
    return vectores[etiquetas == grupo_mayor]



def main(): 
    args = parse_args() 
 
    if args.ref and args.compare: 
        flag = 0
        centroids = [] 
        for model in ["Specter2","Prone"]: 
            
            print("Starting "+ model+" model") 
            df_model = [] 

            if model == "Specter2": 
                flag = 0 
            else: 
                flag = 1 

             
            for ref in ["all","rw","cluster"]: 
                flag_2 = 0
                print("Processing "+ ref) 
                if ref == "all": 
                    path_references = args.ref 
                elif ref == "rw": 
                    path_references = args.related
                else:
                    path_references = args.ref
                    flag_2 = 1
                
                vectors = [] 
                with open(path_references, 'r') as infd:
                    lines = infd.readlines()
                    total_lines = len(lines)
                    for i, line in tqdm(enumerate(lines), total=total_lines, desc='Processing vectors'):
                        rline = line.rstrip()
                        fields = rline.split('\t')
                        if flag == 0:
                            vect = get_vector_hf(' '.join(fields[1:]))
                        else:
                            vect = get_vector_prone(fields[0], "/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model")
                        vectors.append(vect)

                if flag_2 == 1:
                    vectors = clustering_kmeans(vectors,4)

                print("Calculating centroid") 
                new_vector = get_centroid(vectors) 
                centroids.append({"model":model,"ref":ref,"vector": np.array(new_vector)})
 
                cosines, title, idxs = [], [], [] 
                with open(args.compare, 'r') as ff:
                    lines = ff.readlines()
                    total_lines = len(lines)
                    for i, line in tqdm(enumerate(lines), total=total_lines, desc='Processing cosine similarity'):
                        rline = line.rstrip()
                        fields = rline.split('\t')
                        if flag == 0:
                            vector_comp = get_vector_hf(' '.join(fields[1:]))
                        else:
                            vector_comp = get_vector_prone(fields[0], "/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model")
                        
                        cos_output = get_cosine(new_vector, vector_comp)
                        idxs.append(fields[0])
                        title.append(fields[1])
                        cosines.append(cos_output.detach().numpy())
 
                print("Sorting data") 
                sorted_data = sorted(zip(title, cosines, idxs), key=lambda x: x[1], reverse=False) 
                df = pd.DataFrame(sorted_data, columns=['title', 'cosine', 'corpus_id']) 
                df_model.append(df) 
 
            df_1 = df_model[0] 
            df_2 = df_model[1]
            df_3 = df_model[2]
 
            size_df_1 = len(df_1) 
            size_df_2 = len(df_2)
            size_df_3 = len(df_3)
            # Create numeric indices for the x-axis 
            index_1 = range(size_df_1) 
            index_2 = range(size_df_2) 
            index_3 = range(size_df_3) 
 
            # Create the graph 
            print("Creating graph")
            plt.subplot(122) 
            plt.figure(figsize=(16, 12)) 
            plt.plot(index_1, df_1['cosine'], label='All references') 
            plt.plot(index_2, df_2['cosine'], label='Related Work references') 
            plt.plot(index_3, df_3['cosine'], label='Cluster references') 
            plt.xlabel('Index') 
            plt.ylabel('Cosine Similarity') 
            plt.title('Cosine Similarity Curve Comparison') 
            plt.legend() 
            plt.tight_layout() 
            print("Saving graph") 
            plt.savefig(model + '_comparacion_cosine.png') 
            print("Process completed for "+ model)


    # Paso 2: Obtener los vectores "new_vector" de cada elemento del vector principal
    
    vectores_new = [elemento["vector"] for elemento in centroids]

    # Paso 3: Asegurar que todos los vectores tengan la misma longitud (rellenar con ceros si es necesario)
    max_len = max(len(vector) for vector in vectores_new)
    vectores_new_padded = pad_sequences(vectores_new, maxlen=max_len, padding='post', dtype='float32')


    # Convertir la lista de vectores en una matriz NumPy
    X = np.array(vectores_new_padded)


    # Paso 3: Aplicar t-SNE para reducir la dimensionalidad a 3
    tsne = TSNE(n_components=3, perplexity=3, random_state=42)
    vectores_new_3d = tsne.fit_transform(X)

    # Paso 4: Crear el gráfico 3D interactivo con etiquetas "model_ref"
    fig = go.Figure()

    for i, elemento in enumerate(centroids):
        model_ref = f"{elemento['model']}_{elemento['ref']}"
        fig.add_trace(go.Scatter3d(
            x=[vectores_new_3d[i, 0]],
            y=[vectores_new_3d[i, 1]],
            z=[vectores_new_3d[i, 2]],
            mode='markers+text',
            marker=dict(size=6),
            text=model_ref,
            name=model_ref
        ))

    # Configurar el diseño del gráfico
    fig.update_layout(scene=dict(xaxis_title='Dimensión 1',
                                yaxis_title='Dimensión 2',
                                zaxis_title='Dimensión 3'),
                    margin=dict(l=0, r=0, b=0, t=0))

    fig.write_image("grafico_3d.png")



if __name__ == "__main__":
    main()   
