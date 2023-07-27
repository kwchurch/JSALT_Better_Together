## Usage

export JSALTdir=/data3/jsalt2023/
export walkdir=/data3/jsalt2023/semantic_scholar/p.vickers/walks/ (where Globus:/~/semantic_scholar/Peter.Vickers/walk12.zip is extracted)
 
python Predicting_from_Random_Walks.py -o walk_forecasting/
python Predicting_from_Random_Walks.py -i walk_forecasting/ -i walk_forecasting_plots/
