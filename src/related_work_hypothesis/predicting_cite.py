
import pandas as pd
import os
import ast
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from keras.layers import Dropout
import argparse
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="vectores folder", default="/mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/predicting_vectors/")
    args = parser.parse_args()
    return args


def models(input_dim,output_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim))
    return model


def train_model(X, Y, input_dim, output_dim):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model = models(input_dim, output_dim)
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Create a History object to record the training metrics
    history = model.fit(X_train, Y_train, epochs=30, batch_size=32, validation_data=(X_test, Y_test))

    y_pred = model.predict(X_test)
    mse = mean_squared_error(Y_test, y_pred)
    print("Error cuadrático medio (MSE):", mse)

    # Plot the loss and MSE improvement during training
    plot_training_metrics(history)
    
    return model


def test(model,X,Y):
    single_example_index = 4
    single_example = X.iloc[single_example_index].values
    salida = Y.iloc[single_example_index].values
    df_single_example = pd.DataFrame([single_example])
    predicted_output = model.predict(df_single_example)
    predic = predicted_output[0]
    similarity = cosine_similarity(salida.reshape(1, -1),predic.reshape(1, -1))
    print("Similitud del coseno entre los dos vectores:", similarity)


def plot_training_metrics(history):
    # Extract the training and validation loss from the history
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # Create a graph showing the loss function improvement
    plt.figure(figsize=(10, 6))
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig('1.png')


def main():
    
    args = parse_args()

    FILEPATH = os.path.dirname(args.input)
    raw_dirs = set([d for d in os.listdir(FILEPATH)])

    x,z,y = [],[],[]

    for archivo in raw_dirs:
        with open(FILEPATH+"/"+archivo, "r") as file:
            for line in file:
                if line.find("V") == -1:
                    line = line.replace("\n","")
                    line = line.replace("'","")
                    z.append(ast.literal_eval(line.split("\t")[1]))
                    x.append(ast.literal_eval(line.split("\t")[2]))
                    y.append(ast.literal_eval(line.split("\t")[3]))

    df_x = pd.DataFrame(x)
    df_y = pd.DataFrame(y)
    df_z = pd.DataFrame(z)

    print("Total of paper: ", len(df_x))

    #Case 1: all references
    merged_df = pd.concat([df_x, df_y], axis=1)
    model = train_model(merged_df,df_z,560,280)
    model.save('all_modelo.h5')
    test(model,merged_df,df_z)

    #Case 2: all references
    model = train_model(df_x,df_z,280,280)
    model.save('rw_modelo.h5')
    test(model,df_x,df_z)


if __name__ == "__main__":
    main()