import invertedIndexProcess


module = invertedIndexProcess

li = module.invertedIndex()
#li.readFromFile('dataset/andQueryMatch.txt')
#li.readFromFile('dataset/ds_num_1.txt')


from os import path
corpus = path.dirname(__file__)  + "/dataset/corpus/"



#for i in range(1 , 424):
 #   path = corpus + str(i) + ".txt"
  #  li.readFromFile(path)

#li.readFromFile("dataset/ds_num_1.txt")


# query's vector
#print("------- Score -------")

# matching (using frequency in doc) ==> scores



print("\nIndex... \n")
#li.presentInvertedIndex()

print("\nKeywords... \n")
#li.presentKeywordsIndex()

print("\nindex by (keyword , occurrence)... \n")
#li.presentKeywordsOccur()

#print("\nindex by (keyword , Total occurrence) ordered by occurrence ... \n")
#li.presentIndexOrderByOccur()



