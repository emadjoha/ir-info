import re
import
class Intersection:

    def __init__(self):
        self.inrSecLists = []
        self.taked_terms = []
        self.ranked_result = {"sum_tf_idf": [], "vs_freq": [], "vs_tf_idf": []}
        self.termsDueLevels = {}
        self.takenTermsDueLevel = {}
        self.topLevelOfTerms = 0

    def clearForQuery(self):
        self.ranked_result = {"sum_tf_idf": [], "vs_freq": [], "vs_tf_idf": []}
        self.termsDueLevels = {}
        self.takenTermsDueLevel = {}
        self.topLevelOfTerms = 0


    def matchWords(self , index , query ):

        self.inrSecLists = []
        self.taked_terms = []
        for word in query.inverted_lists.keys():
            print("Check for : " , word)
            if word in index.inverted_lists :
                print("{} is Exist ... ".format(word))
                self.inrSecLists.append(set(index.inverted_lists[word]))
                self.taked_terms.append(word)

            # word is not found in index
            #else :
            #    self.inrSecLists.append(set())

        return self.inrSecLists

    def matchByAnd(self , first , second ):
        self.inrSecLists[second] =  self.inrSecLists[second].\
            intersection(self.inrSecLists[first])
        print("After Intersection =>> {}".format(self.inrSecLists[second]))

    def matchByOr(self, first, second):
        self.inrSecLists[second] = self.inrSecLists[second].\
            union(self.inrSecLists[first])
        print("After Union =>> {}".format(self.inrSecLists[second]))


    def matchByNot(self, first, second):
        self.inrSecLists[second] = self.inrSecLists[first]. \
            difference(self.inrSecLists[second])
        print("After Difference =>> {}".format(self.inrSecLists[second]))



    def matchOperators(self , BiOprt , index ):

        if BiOprt == 'and':
            self.matchByAnd(index, index + 1)

        if BiOprt == 'or':
            self.matchByOr(index, index + 1)

        if BiOprt == 'not':
            self.matchByNot(index, index + 1)



    def takeAndLeaf(self , term_id , taken_terms , taken_doc_ids ):


        if( term_id == len(self.taked_terms)):
            print("#" , taken_terms)
            print("$" , taken_doc_ids)
            # take action  ....
            self.getherTakenTerms(taken_terms , taken_doc_ids )
            return 1

        # take (Term)
        taken_terms.append( self.taked_terms[term_id] )
        taken_doc_ids.append(self.inrSecLists[term_id])
        self.takeAndLeaf(term_id+1 , taken_terms , taken_doc_ids )
        taken_terms.pop()
        taken_doc_ids.pop()

        # leave (Term)
        self.takeAndLeaf(term_id+1 , taken_terms , taken_doc_ids )


    def intersectTakenTerms(self , taken_terms , taken_doc_ids):

        length = len(taken_terms)
        if (not length):
            return -1

        intersection_result = set(taken_doc_ids[0])
        index = 0
        while (index < length - 1):
            intersection_result = intersection_result.intersection(taken_doc_ids[index + 1])
            index += 1

        if (not len(intersection_result)):
            return set()

        return intersection_result


    def getherTakenTerms(self , taken_terms , taken_doc_ids ):

        copy_taken_terms = set()
        length = len(taken_terms)

        if( not length ) :
            return

        for term in taken_terms :
            copy_taken_terms.add(term)

        self.topLevelOfTerms = max(length , self.topLevelOfTerms)


        # first intersect the taken terms
        result = self.intersectTakenTerms(taken_terms , taken_doc_ids)


        if length not in self.termsDueLevels.keys() :
            self.termsDueLevels[length] = []
            self.takenTermsDueLevel[length] = []

        self.termsDueLevels[length].append(result)
        self.takenTermsDueLevel[length].append(copy_taken_terms)


    def rankTakenTerms(self , matcher):
        top = self.topLevelOfTerms
        while top > 0 :
            if( top in self.termsDueLevels.keys() ):
                if( len(self.termsDueLevels[top]) ):
                    items = len(self.termsDueLevels[top])
                    index = 0
                    while index < items :
                        matcher.ranker.ranking( self.termsDueLevels[top][index] , self.takenTermsDueLevel[top][index],self.ranked_result )
                        index+=1
            top-=1


    def intersectMatchedDocs(self , matcher):
            self.clearForQuery()
            self.takeAndLeaf(0,[],[])
            print("------------Rank ---------------")
            self.rankTakenTerms(matcher)
            print(self.ranked_result)
            return self.ranked_result



