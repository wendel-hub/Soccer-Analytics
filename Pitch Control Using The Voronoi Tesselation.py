#!/usr/bin/env python
# coding: utf-8

# # Importing The Needed Libraries

# In[3]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch


# # Creating a dummy coordinate to plot the particular scenario in question

# In[4]:


#Create the dummy dataset
barca_x = [93,96,99,102,104,95,86,79,89]
barca_y = [9,22,33,44,56,63,52,33,22]
barca = list(np.zeros((9,),dtype = int))

cadiz_x = [99,100,102,104,104,102,97,98,94,77]
cadiz_y = [14,22,33,43,46,55,37,27,21,45]
cadiz = list(np.ones((10,),dtype = int))


# In[5]:


#Create the dataframe

df = pd.DataFrame({
    'x': barca_x + cadiz_x,
    'y': barca_y + cadiz_y,
    'team': barca+cadiz
})

df.head()


# In[6]:


#Create the points for the Voronoi
points = np.column_stack((df.x,df.y))

barca_df = df[df['team']==0]
cadiz_df = df[df['team']==1]


# # Creation of The Visual Using The Voronoi Tesselation to Show Pitch Control

# In[8]:


#Create the visual
fig,ax = plt.subplots(figsize=(13,8.5))
fig.set_facecolor('#38383b')
ax.patch.set_facecolor('#38383b')

pitch = Pitch(pitch_type = 'statsbomb',orientation = 'vertical',pitch_color = '#38383b',half = True
              ,line_color = 'white',constrained_layout = False,tight_layout = False)
ax.scatter(barca_df.x,barca_df.y,c= 'red')
ax.scatter(cadiz_df.x,cadiz_df.y,c= 'yellow')
pitch.draw(ax = ax)

x= df.x
y= df.y
team1, team2 = pitch.voronoi(x,y,df.team)

t1 = pitch.polygon(team1,ax=ax,facecolor = 'yellow',ec = 'yellow',lw =3, alpha = 0.3)
t2 = pitch.polygon(team2,ax=ax,facecolor = 'blue',ec = 'blue',lw =3, alpha = 0.3)


# Thank You!
