## Link Prediciton Evaluation
We consider a simple setting to evaluate the train and test prediction capabilities of our Paper representation models.
As detailed in https://github.com/kwchurch/JSALT_Better_Together/blob/main/projects/link_prediction_from_random_walks.md, we take random walks across the citation graph to form pairs of papers with minimum number of hops in [1,4]. We then record the (time) bin of each paper and the cosine similarity between the two papers with all text and graph embedding models. 

The task we define to assess model cabability is to predict from the cosine of the embeddings whether or not the papers are 1 or 2-4 hops apart. Given a list of paper0, paper1, their bins and their cosine similarities for a given model, we learn a threshold value such that cosine_sim > threshold => papers are one-hop. We use a logistic regression over the first 500K random walks to calculate this value. We then report the accuracy at predicting 1 vs 2-4 hops over the remaining approx 3M random walks. We record the overall accuracy, and the accuracy per bin, which we define as the whichever bin is higher of the two papers at each end of the walk.

This allows us to report the in-train representation ability of models by looking into bins the model was trained on and the forecast prediciton ability of models by looking at performance on bins as they move out from the train/test cutoff. 

As that 69.4% of all walks are 2-4 hops and cases where paper representations cannot be formed are given cosine similarities of -1 the accuracy paradox is a problem for establishing performance. We therefore start with a policy of omitting all random walks where embeddings for both papers cannot be found.

Here we show the forecasting performance with the ProNE model, using the use_references='when necessary' setting for forming paper embeddings 
```
![Heatmap Plot of ProNE Forecasting](prone_when_necessary_heatmap.jpg?raw=true)
`
![Training Bins vs Overall Accuracy](prone_when_necessary_lineplot.jpg?raw=true)
```
