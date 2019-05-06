import xml.sax


class FirstTestDSProcess(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.num = ""
        self.story = ""
        self.blogs08day = ""
        self.counter = 0

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "top":
            self.counter += 1
            print ("({})  ".format(self.counter))

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "num":
            print("num : {}".format(self.num) )
        elif self.CurrentData == "story":
            print("story : {}".format(self.story) )
        elif self.CurrentData == "blogs08day":
            print("blogs08day : {}".format(self.blogs08day) )
            testDSF1.write(self.num + " " +
                           self.story + " " +
                           self.blogs08day + "\n" )

        self.CurrentData = ""


    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "num":
            self.num = content
        elif self.CurrentData == "story":
            self.story = content
        elif self.CurrentData == "blogs08day":
            self.blogs08day = content



# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = FirstTestDSProcess()
parser.setContentHandler(Handler)

testDSF1 = open("dataset/testDS_num1.txt", "a")
parser.parse("dataset/testDS_num1.xml")
testDSF1.close()













import nltk
import fuzzy
soundex = fuzzy.Soundex(4)

text = nltk.word_tokenize("ashraf ali And now for something completely different")
words=nltk.pos_tag(text)
print(words)
nouns=[]
for word in words:
  if (word[1]=='NN'):
    nouns.append(word[0])
  elif (word[1]=='FN'):
    nouns.append(word[0])
  elif (word[1]=='NP'):
    nouns.append(word[0])
print(nouns)
nounaftersound=[]
for noun in nouns:
  nounaftersound.append(soundex(noun))
print(nounaftersound)