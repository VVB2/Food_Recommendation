import pandas as pd 
from os import path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.utils import gen_batches

df = pd.read_csv("./data/minified_data.csv")

df["NER"] = df["NER"].apply(lambda x: x[1:len(x)-2])

df["title"] = df["title"].str.strip()

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0.0, stop_words='english')
tfidf_matrix = tf.fit_transform(df["NER"])

def cos_compare(matrix):
   slices = gen_batches(matrix.shape[0], 1000)
   for i in slices:
       x = linear_kernel(matrix[i],matrix)
       yield x

if not path.exists('./data/cosine_sim.csv'):
    try:
        for x in cos_compare(tfidf_matrix):
            print('Processed 1000 rows of {}:'.format(tfidf_matrix.shape[0]))
            pd.DataFrame(x).to_csv('./data/cosine_sim.csv', header=False,index=False,mode='a')
    finally:
        cosine_sim = pd.read_csv('./data/cosine_sim.csv', header=None)
else:
    cosine_sim = pd.read_csv('./data/cosine_sim.csv', header=None)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

df = df.reset_index()
titles = df['title']
indices = pd.Series(df.index, index=df['title'])

def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    recipe_indices = [i[0] for i in sim_scores]
    df_titles = pd.DataFrame(titles.iloc[recipe_indices])
    return df_titles.to_numpy()
    