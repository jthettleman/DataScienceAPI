#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup as bs


# In[2]:


startID = "76561198330189125" 
key = "927F6B4A4072151FAF4BD03CAE7F8C74"

friendFunction = "GetFriendList"
banFunction = "GetPlayerBans"
summaryFunction = "GetPlayerSummaries"

summaryVersion = "v0002"
friendVersion = "v0001"
banVersion = "v1"

whole ="http://api.steampowered.com/ISteamUser/"+friendFunction+"/"+friendVersion+"/?key="+key+"&steamid="+startID+"&format=XML"
response = requests.get(whole)

starterBowl = bs(response.content,"lxml")


# In[3]:






def isBanned(SteamID):
    banCall = "http://api.steampowered.com/ISteamUser/"+banFunction+"/"+banVersion+"/?key="+key+"&steamids="+SteamID+"&format=XML"
    banCallReq = requests.get(banCall)
    banBowl = bs(banCallReq.content,"lxml")
    
    for tag in banBowl.findAll("vacbanned"):
        if tag.text == "false":
            return False
        elif tag.text == "true":
            return True

    
    
def findFriendCodes(targetID):
    
    print("targetID", targetID)
    theFriends = []
    friendCall ="http://api.steampowered.com/ISteamUser/"+friendFunction+"/"+friendVersion+"/?key="+key+"&steamid="+targetID+"&format=XML"
    friendCallReq = requests.get(friendCall)
    friendBowl =  bs(friendCallReq.content,"lxml")

    for tag in friendBowl.find_all("steamid"):
        theFriends.append(tag.text)
    return(theFriends)

    
    
    
def findIDName(targetID):
    SummaryCall ="http://api.steampowered.com/ISteamUser/"+summaryFunction+"/"+summaryVersion+"/?key="+key+"&steamids="+targetID+"&format=XML"
    SummaryCallReq = requests.get(SummaryCall)
    SummaryBowl = bs(SummaryCallReq.content,"lxml")
    for tag in SummaryBowl.findAll("personaname"):
        return(tag.text)

    
    
def friendTree(doneList, bannedPerson):
    tree = ""
    for person in doneList:
        userName = findIDName(person)
        tree = tree+" "+userName+" > "
    tree+= bannedPerson
    return tree
    

    
  
    
    
    
    
    
    
    
   
    


# In[4]:


doneBefore = []

friendList = []
treeLevel = 0 
foundBan = False
rootID = startID
counter = 0
pastStart = False
bannedFriend = ""
while foundBan != True:
    
    
    doneBefore.append(rootID)
    treeLevel+=1
    print("TREE LEVEL: ", treeLevel)
    
    
    
    
    friendList = findFriendCodes(rootID)
    #print(friendList)
    amountOfFriends = len(friendList)
    print("Amount of friends: ",amountOfFriends)
    print("-----------------------------------------------")
    
    for friend in friendList:
        foundBan = isBanned(friend)
        if foundBan == True:
            print(isBanned(friend), friend)
            bannedFriend = findIDName(friend)
            print(friendTree(doneBefore, bannedFriend))
            break
        print(isBanned(friend), friend)
        
    
    newID = friendList[counter]
    #print("new",newID)
    
    while newID == rootID:
        for ID in doneBefore:
            if newID == ID:
                counter+=1
                newID = friendList[counter]
        
        
    #print("new2",newID)
    #print("root",rootID)
    rootID = newID
    #print("root2",rootID)    
    
    
    
    counter +=1
    


# In[ ]:


# In[ ]:




