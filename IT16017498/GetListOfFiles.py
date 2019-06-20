import re
import keyword




filePath="D:/CDAP/PyGitHub/ARIMA.py"
def CalculateCognitiveWeight(line):
    
    cognitiveWeight = 0
    res = re.findall(r'[a-zA-Z]+', line)

    for w in res:
      if (w == "if") or  (w == "elif") or (w == "elseif") or (w == "else") or  (w=="then") or (w == "case"):
        cognitiveWeight = cognitiveWeight + 2
      elif (w == "for") or (w == "while") or (w == "do") or (w == "repeat") or (w == "until"):
        cognitiveWeight = cognitiveWeight + 3 
      elif (w == "continue"):
        cognitiveWeight = cognitiveWeight + 1

    return cognitiveWeight

def countIdentifiers(line):
    wordList = []
    commonkeywords=['for' ,'do','while','if','else','elseif','elif','switch','case','continue','pass','try','catch',
                   'continue','int','double','float','finally' ,'from','return','null','=']
    keywords1 = keyword.kwlist
    keywordsJava= ['import' ,'from','abstract','boolean','break','byte','case','catch','char','class','continue','default','final','private',
                  'protected','throws','void']
    #keywordJavaScript = []
    #keywordC=[]
    res = re.findall(r'[a-zA-Z]+', line)
    for w in res:
        if (w not in keywords1) and (w not in keywordsJava) and (w not in commonkeywords):
           wordList.append(w)
 
           
    Identifiers = set (wordList)
    return len(Identifiers)

def CalculateArithmeticOperartors(line):
    c1 = 0
    if '+' in line:
        c1= c1 + 1
    if '-' in line:
        c1 = c1 + 1
    if '*' in line:
        c1 = c1 + 1
    if '/'in line:
        c1 = c1 + 1
    if '%' in line:
        c1 = c1 + 1
    if '++' in line:
        c1 = c1 + 1
    if '+=' in line:
        c1 = c1 + 1
    if '-=' in line:
        c1 = c1 + 1
    if '*-' in line:
        c1 = c1 + 1    
    if '/=' in line:
        c1 = c1 + 1
    if '%=' in line:
        c1 = c1 + 1
    if '--' in line:
         c1 = c1 + 1

      
    return c1

   
def CalculateLogicalOperators(line):
    c2 = 0
    if '!' in line:
      c2 = c2 + 1
    if '!=' in line:
      c2 = c2 + 1
    if '<' in line:
      c2 = c2 + 1
    if '<=' in line:
      c2 = c2 + 1
    if '>' in line :
       c2 = c2 + 1
    if '>=' in line:
       c2 = c2 + 1
    if '&&' in line:
       c2 = c2 + 1
    if '||' in line:
        c2 = c2 + 1
    if '==' in line:
        c2 = c2 + 1
    if 'or' in line:
        c2 = c2 + 1
    if 'and' in line:
        c2 = c2 + 1
    
    return c2      
    

#Open the file for reading
LinesOfCode= 0

with open(filePath, 'r') as filehandle:
    TotalDistinctIdentifiers = 0
    TotalCognitiveWeight = 0
    filecontent = filehandle.readlines()
    WordContent = str(filecontent)
    SplittedWord = WordContent.split(' ')
    TotalDistinctOperators =CalculateArithmeticOperartors(SplittedWord) + CalculateLogicalOperators(SplittedWord)
    print("Total Operators " + str(TotalDistinctOperators))
    for line in filecontent:
        LinesOfCode =LinesOfCode + 1
        TotalDistinctIdentifiers = TotalDistinctIdentifiers + countIdentifiers(line)

        CalculateCognitiveWeight(line)
        TotalCognitiveWeight = TotalCognitiveWeight + CalculateCognitiveWeight(line)

    print(TotalDistinctIdentifiers)
    print("LOC " + str(LinesOfCode))
    print(TotalCognitiveWeight)
   
    MetricValue = (TotalDistinctOperators + TotalDistinctIdentifiers + TotalCognitiveWeight) / LinesOfCode
    IdentifierPercentage = (TotalDistinctIdentifiers /LinesOfCode) * 100 
    CognitiveWeightPercentage = (TotalCognitiveWeight /LinesOfCode) * 100
    print(IdentifierPercentage)
    print(CognitiveWeightPercentage)
    