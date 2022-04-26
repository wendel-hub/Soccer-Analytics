#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns


def draw_soccer_pitch(figsize=(9, 6)):
    """
    Function that plots a scaled soccer pitch of length 120*90 metres which 
    are the maximum dimensions allowed by FIFAs "Laws Of The Game"
    """
    rect = patches.Rectangle((-1, -1), 132, 92, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)
    # Main pitch markings, ie sidelines, penalty area and halfway line
    plt.plot([0, 0,  0, 120, 120, 0,     0,  16.5,  16.5,     0,     0,   5.5,   5.5, 
                  0,  0, 60, 60, 120,   120, 103.5, 103.5,   120,   120, 114.5, 114.5,   120], 
             [0, 0, 90,  90,   0, 0, 25.85, 25.85, 66.15, 66.15, 55.15, 55.15, 36.85, 
              36.85, 90, 90,  0,   0, 25.85, 25.85, 66.15, 66.15, 55.15, 55.15, 36.85, 36.85], color='white')
    
    # Secondary pitch markings, ie penalty spots, centre circle etc
    plt.plot([11, 11.5],[45, 45], color='white')
    plt.plot([109, 108.5],[45, 45], color='white')
    
    centre_circle = patches.Circle([60, 45], 9.15, edgecolor='white', fill = False)
    ax.add_patch(centre_circle)
    
    left_arc = patches.Arc([16.5, 45], 9.15, 16, theta1=270.0, theta2=90.0, color='white')
    ax.add_patch(left_arc)
    right_arc = patches.Arc([103.5, 45], 9.15, 16, theta1=90.0, theta2=270.0, color='white')
    ax.add_patch(right_arc)
    
    bl_corner = patches.Arc([0, 0], 2.5, 2.5, theta1=0.0, theta2=90.0, color='white')
    tl_corner = patches.Arc([0, 90], 2.5, 2.5, theta1=270.0, color='white')
    br_corner = patches.Arc([120, 0], 2.5, 2.5, theta1=90.0, theta2=180.0, color='white')
    tr_corner = patches.Arc([120, 90], 2.5, 2.5, theta1=180.0, theta2=270.0,color='white')
    ax.add_patch(bl_corner)
    ax.add_patch(tl_corner)
    ax.add_patch(br_corner)
    ax.add_patch(tr_corner)
    
    plt.xlim(-1, 121)
    plt.ylim(-1, 91)
    plt.axis('off')    

    return fig, ax


# In[2]:


draw_soccer_pitch()
plt.show()


# In[3]:


data = pd.read_csv(r'C:\Users\wendel.amoo\Desktop\Data Science\Football Analytics\open-data-master\data\events\8649.csv')
starting_11 = data[data['type/name'] == 'Pass']
starting_11.head()


# In[4]:


starting_11 = starting_11[['team/name','possession_team/id','player/name','position/name','location/0','location/1','type/name','pass/outcome/name','pass/end_location/0','pass/end_location/1']]
starting_11.head()


# In[5]:


#Combining Coordinates for plotting
starting_11['Pass_location'] = [[x,y] for x,y in zip(starting_11['location/0'],starting_11['location/1'])]
starting_11['End_Pass_location'] = [[x,y] for x,y in zip(starting_11['pass/end_location/0'],starting_11['pass/end_location/1'])]
starting_11.drop(['location/0','location/1','pass/end_location/0','pass/end_location/1'],axis = 1)
starting_11.head()


# In[6]:


starting_11['team/name'].value_counts()


# In[7]:


starting_11['player/name'].value_counts()


# In[8]:


Pogpass = starting_11[starting_11['player/name']=='Paul Pogba']
Pogpass.head()


# In[14]:


x_coord = [i[0] for i in Pogpass['Pass_location']]
y_coord = [i[1] for i in Pogpass["Pass_location"]]

def draw_pitch(ax):
    pitch = plt.Rectangle([0,0], width = 120,height = 80,fill = False,color ='black')
    
    LeftPenalty = plt.Rectangle([0,22.3], width = 14.6, height = 35.3,fill = False,color ='black')
    RightPenalty = plt.Rectangle([105.4,22.3], width = 14.6, height = 35.3,fill = False,color ='black')
    
    midline = plt.axvline(60,0.03,0.97,color ='black')
    
    LeftSixYard = plt.Rectangle([0,32], width = 4.9, height = 16,fill = False,color ='black')
    RightSixYard = plt.Rectangle([115.1,32], width = 4.9, height = 16,fill = False,color ='black')
    
    centrecircle = plt.Circle((60,40),8.1,fill = False,color ='black')
    centrespot = plt.Circle((60,40),0.71,color ='black')
    
    LeftPenSpot = plt.Circle((9.7,40),0.6,color ='black')
    RightPenSpot = plt.Circle((110.3,40),0.71,color ='black')
    
    leftArch = patches.Arc((9.7,40),height = 16.2,width = 16.2,angle = 0, theta1 = 310, theta2 = 50,color ='black')
    RightArch = patches.Arc((110.3,40),height = 17,width = 16.2,angle = 0, theta1 = 130, theta2 = 230,color ='black')
    
    element = [pitch,LeftPenalty,RightPenalty,LeftSixYard,RightSixYard,centrecircle,centrespot,LeftPenSpot,RightPenSpot,leftArch,RightArch]
    for i in element:
        ax.add_patch(i)


# In[19]:


fig = plt.figure()
fig.set_size_inches(10,7)
ax = fig.add_subplot(1,1,1)
draw_pitch(ax)
sns.kdeplot(x_coord, y_coord, shade = "True", color = "green", n_levels = 100)
plt.scatter(x_coord,y_coord,color = 'red')
for i in range(len(Pogpass)):
    #ax.annotate ("draw an arrow from a current position to pass_end_location")
    ax.annotate("", xy = (Pogpass.iloc[i]['End_Pass_location'][0], Pogpass.iloc[i]['End_Pass_location'][1]), xycoords = 'data',
               xytext = (Pogpass.iloc[i]['Pass_location'][0], Pogpass.iloc[i]['Pass_location'][1]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"))
    ax.set_title('Paul Pogba Passing Location')
plt.ylim(-2,82)
plt.xlim(-2,122)
plt.axis('off')
plt.show()


# Thank YOU!

# In[ ]:




