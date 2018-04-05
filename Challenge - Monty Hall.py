
# coding: utf-8

# One of the classic problems in this space is referred to as the Monty Hall Problem. Some people even use this as an interview question! It is deceptively simple, and really digging into it reveals a myriad of approaches and some serious applications of conditional probability. The story goes like this:
# 
# You are on a game show and given the choice of whatever is behind three doors. Behind one door is a fantastic prize (some examples use a car, others use cash) while behind the other two doors is a dud (some examples say a goat, others say it's just empty). You pick a door. Then the host opens one of the other two doors to reveal a dud. But here's the wrinkle: the host now gives you the opportunity to switch your door. What should you do?
# 
# Write up some notes on this problem, including how you think Bayes' Rule might apply. Drop a link to your notes below and discuss it with your mentor.

# The table below shows all the epossible outcomes in order for a player to win the game. The first column represents all the choices at the beggining. The second column shows all the location possibilities of the prize.The last column shows whether the player should choose to stay or switch after a door is removed by the host. 

# In[2]:


import pandas as pd

outcomes = pd.DataFrame()
outcomes['Choice'] = ['1', '1', '1', '2', '2', '2', '3', '3', '3']
outcomes['Prize'] = ['1', '2', '3', '1', '2', '3', '1', '2', '3']
outcomes['Stay or Switch'] = ['stay', 'switch', 'switch', 'switch', 'stay', 'switch', 'switch', 'switch', 'stay']
    

print(outcomes)


# if the player chooses to "switch" their odds of winning are 6 out of 9(sum all the "switch" outcomes) however, if they choose to "stay" their odds are 3 out of 9.
