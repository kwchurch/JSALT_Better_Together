## Usage

export JSALTdir=/data3/jsalt2023/
export walkdir=/data3/jsalt2023/semantic_scholar/p.vickers/walks/ (where Globus:/~/semantic_scholar/Peter.Vickers/walk12.zip is extracted)

python Predicting_from_Random_Walks.py -o prone_forecast_guess -t 4 -m guess 
python Random_Walks_Plot.py -i prone_forecast_guess/ -o prone_forecast_guess_plots/

python Predicting_from_Random_Walks.py -o prone_forecast_specter1 -t 4 -m specter1 
python Random_Walks_Plot.py -i prone_forecast_specter1/ -o prone_forecast_specter1_plots/
