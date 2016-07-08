#from __future__ import division
import pandas as pd
import numpy as np
import operator


path = 'https://raw.githubusercontent.com/ksanju0/IS643/master/u.data'
columns = ['user_id','item_id','rating','timestamp']
mat1 = pd.read_csv(path, names=columns, delimiter='\t')
p1 = mat1.as_matrix()
print p1
#Tranform the input into numpy array
user_item_matrix = np.zeros((943,1682), dtype=np.int)
user_item_matrix -= 1
for x in p1:
    user_item_matrix[x[0]-1][x[1]-1] = x[2]

user_item_matrix[268][126] = -1
user_avg_rat = {} ########## Average user rating
user_count = 0
user_sum = 0
for row in range(user_item_matrix.shape[0]):
    user_sum = 0
    user_count = 0
    for col in range(user_item_matrix.shape[1]):
        if user_item_matrix [row][col] != -1:
            user_count += 1
            user_sum += user_item_matrix [row][col]
    user_avg_rat[row] = user_sum / float(user_count)


item_avg_rat = {}
item_count = 0
item_sum = 0
for row in range(user_item_matrix.transpose().shape[0]):
    item_count = 0
    item_sum = 0
    for col in range(user_item_matrix.transpose().shape[1]):
        if user_item_matrix.transpose() [row][col] != -1:
            item_count += 1
            item_sum += user_item_matrix.transpose()[row][col]
    item_avg_rat [row] = item_sum / float(item_count)

####################################################
# Performing SVD to get matrix U , S and V
S = np.zeros((943,1682), dtype= np.int)
U, _S, V = np.linalg.svd(user_item_matrix)
np.fill_diagonal(S,_S)
V = V.transpose()
##################################################
# Get the rank two approximation of U, S and V

U = U[:,[0,1]]
S = S[:,[0,1]]
S = S[[0,1],:]
V = V[[0,1],:]

####################################################
# Cosine similarity
def cosine_similarity(arr1,arr2):
   ansh = np.dot(arr1,arr2)
   ched = np.linalg.norm(arr1)*np.linalg.norm(arr2)
   ans = ansh / float(ched)
   return ans
####################################################3
# Find most similar users to user 269

user = 268 # user 269

row_count = 0
user_sim_dict = {}
for row in U:
    if row_count == user:
        row_count += 1
        continue
    sim = cosine_similarity(U[user], row)
    user_sim_dict[row_count] = sim
    row_count += 1

sorted_user_sim_dict = sorted(user_sim_dict.items(), key = operator.itemgetter(1), reverse= True)
print 'Top 5 users that are similar to 269: Format:(userID-1, similarity)'
print sorted_user_sim_dict[0:5:1]

###############################################################
# Find most similar items to item 127

item = 126 #item 127
V = V.transpose()
row_count = 0
item_sim_dict = {}
for row in V:
    if row_count == item:
        row_count += 1
        continue
    sim = cosine_similarity(V[item], row)
    item_sim_dict[row_count] = sim
    row_count += 1

sorted_item_sim_dict = sorted(item_sim_dict.items(), key = operator.itemgetter(1), reverse= True)
print 'Top 5 item that are similar to 127: Format:(ItemId-1, similarity)'
print sorted_item_sim_dict[0:5:1]
##################################################################
# Module to check the average user or item rating

###################################################################
#predict the user-based similarity using SVD:
neighbourhood_size = 5
user_avg_rat_main = user_avg_rat[268]
local_sum = 0
denominator = 0
for n in range(neighbourhood_size):
    if user_item_matrix[sorted_user_sim_dict[n][0]][item] > -1:
        local_sum += (sorted_user_sim_dict[n][1])*(user_item_matrix[sorted_user_sim_dict[n][0]][item] - user_avg_rat[sorted_user_sim_dict[n][0]])
    denominator += sorted_user_sim_dict[n][1]

user_based_predicted_value_with_svd = user_avg_rat_main+ (local_sum / float(denominator))
print 'User based predicted rating with SVD: '+str(user_based_predicted_value_with_svd)

###################################################################
#predict the item-based similarity using SVD:
user_item_matrix = user_item_matrix.transpose()
neighbourhood_size = 5
item_avg_rat_main = item_avg_rat[126]
local_sum = 0
denominator = 0
for n in range(neighbourhood_size):
    if user_item_matrix[sorted_item_sim_dict[n][0]][user] > -1:
        local_sum += (sorted_item_sim_dict[n][1])*(user_item_matrix[sorted_item_sim_dict[n][0]][user] - item_avg_rat[sorted_item_sim_dict[n][0]])
    denominator += sorted_item_sim_dict[n][1]

item_based_predicted_with_svd = item_avg_rat_main + (local_sum/ float(denominator))
print 'Item based predicted rating with SVD: '+ str(item_based_predicted_with_svd)



