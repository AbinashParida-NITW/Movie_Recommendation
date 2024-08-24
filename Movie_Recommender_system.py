#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


credits=pd.read_csv("tmdb_5000_credits.csv")
movies=pd.read_csv("tmdb_5000_movies.csv")


# In[3]:


credits.head(1)


# In[4]:


movies.head(1)


# In[5]:


movies.shape


# In[6]:


credits.shape


# In[7]:


movies=movies.merge(credits,on="title")


# In[8]:


movies.shape


# In[9]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[10]:


movies.head(1)


# In[11]:


movies.shape


# In[12]:


movies.dropna(inplace=True)


# In[13]:


#null values present or not if present remove them
movies.isnull().sum()


# In[14]:


movies.duplicated().sum()


# In[15]:


movies.head(1)


# In[16]:


movies.iloc[0]


# In[17]:


movies.iloc[0].genres 


# In[18]:


import ast


# In[19]:


def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L


# In[20]:


movies["genres"]=movies["genres"].apply(convert)


# In[21]:


movies["keywords"]=movies["keywords"].apply(convert)


# In[22]:


def convert3(obj):
    L=[]
    count=3
    for i in ast.literal_eval(obj):
        if count !=0:
            L.append(i["name"])
            count-=1
        else:
            break
    return L


# In[23]:


movies["cast"]=movies["cast"].apply(convert3)


# In[24]:


movies.head()


# In[25]:


movies["crew"].iloc[0]


# In[26]:


def fetch_Director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i["job"]=="Director":
            L.append(i["name"])
            break
    return L


# In[27]:


movies["crew"]=movies["crew"].apply(fetch_Director)


# In[28]:


movies.head()


# In[29]:


movies["overview"].iloc[0]


# In[30]:


#overview is a sting covert it to list so that we can concatinate 
movies["overview"]=movies["overview"].apply(lambda x: x.split())


# In[31]:


movies.head()


# In[32]:


movies["genres"]=movies["genres"].apply(lambda x:[i.replace(" ","") for i in x])
movies["keywords"]=movies["keywords"].apply(lambda x:[i.replace(" ","") for i in x])
movies["cast"]=movies["cast"].apply(lambda x:[i.replace(" ","") for i in x])
movies["crew"]=movies["crew"].apply(lambda x:[i.replace(" ","") for i in x])


# In[33]:


movies.head()


# In[34]:


movies["tags"]=movies["overview"]+movies["genres"]+movies["keywords"]+movies["cast"]+movies["crew"]


# In[35]:


movies.head()


# In[36]:


new_df=movies[["movie_id","title","tags"]]


# In[37]:


new_df["tags"]=new_df["tags"].apply(lambda x:" ".join(x))


# In[38]:


new_df.head()


# In[39]:


new_df["tags"].iloc[0]


# In[40]:


new_df["tags"]=new_df["tags"].apply(lambda x:x.lower())


# In[41]:


new_df["tags"].iloc[0]


# In[42]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[43]:


vector = cv.fit_transform(new_df['tags']).toarray()


# In[44]:


vector[0]


# In[45]:


import nltk


# In[46]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[47]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[48]:


stem("in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action adventure fantasy sciencefiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d samworthington zoesaldana sigourneyweaver jamescameron'")


# In[49]:


new_df["tags"]=new_df["tags"].apply(stem)


# In[50]:


from sklearn.metrics.pairwise import cosine_similarity


# In[51]:


similarities=cosine_similarity(vector)


# In[52]:


similarities[1]# it will give the similarity of the i th index movies to all moviews.here the index is 1


# In[53]:


sorted(list(enumerate(similarities[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[54]:


def recommend(movie):
    movie_index=new_df[new_df["title"]==movie].index[0]
    distance=similarities[movie_index]
    movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


# In[55]:


# calculate index new_df[new_df["title"]=="Avatar"].index[0]
#new_df.iloc[539].title


# In[56]:


recommend("Batman Begins")


# In[57]:


import pickle


# In[58]:


pickle.dump(new_df,open("movies.pkl","wb"))


# In[59]:


import os
print(os.getcwd() )
#path of directory


# In[60]:


# name of all movies
new_df["title"].values


# In[61]:


pickle.dump(new_df.to_dict(),open("movies_dict.pkl","wb"))


# In[62]:


pickle.dump(similarities,open("similarities.pkl","wb"))


# In[ ]:




