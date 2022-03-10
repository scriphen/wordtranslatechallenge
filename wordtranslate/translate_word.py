import pandas as pd
import re
import time
import os, psutil


# Program Start
start_time=time.time()    ## Current Time capture
print("Process Started ")
# Step 0 : Read Find words txt
try :
    with open('find_words.txt', 'r') as file:  # Read txt file
        findwords = [line.rstrip('\n') for line in file]
        #print(findwords)

## Step 1 - Read french Dictonary file

    frenchdict = pd.read_csv('french_dictionary.csv', header=None)   ## Read CSV file
    column1 = frenchdict[0].to_list()   # Read Column1 ( English word ) and keep it in List
    column2 = frenchdict[1].to_list()   # Read Column2 ( French word ) and keep it in List
    fulldict_temp = dict(zip(column1,column2))  # Add Key ,value into Dict

    # Select only  words which are in "find_words.txt" for further processing
    fulldict=dict()
    for findword in findwords:
        fulldict[findword] = fulldict_temp[findword]
    #print(fulldict)


    # Step 2  Read Text file and replace the french word instead of English word
    with open('t8.shakespeare.txt', 'r') as file:      # Read txt file
        data = file.read()
        numberofoccurance =[]
        lst_english=[]
        lst_french =[]
        for key in fulldict:
            lst_english.append(key)
            lst_french.append(fulldict[key])
            numberofoccurance.append(len(re.findall(key, data)))
            data = data.replace(key, fulldict[key])

    newfile = open("t8.shakespeare.translated.txt", "w")
    newfile.write(" %s " % data)
    newfile.close()



    # Step 3 : Write Number of occurance of each word into separate file
    numberofocc_dict=[{'English':el, 'French':fl, 'Frequency':ol} for el,fl,ol in zip(lst_english,lst_french,numberofoccurance)]
    df = pd.DataFrame (numberofocc_dict, columns = ['English','French','Frequency'])
    df.to_csv("frequency.csv", index=None)



    end_time = time.time()
    totaltime=end_time - start_time   # total time in Seconds

    # Step 4 : Write Performance file

    performancetxt = open("performance.txt", "w")
    processedtime = "Time to process: " + str(totaltime) + " Sec"
    # .rss return value in  bytes to convert bytes into MB formula => Value /  (1024*1024)  . Eg  ( (1024*1024) bytes = 1 megabyte
    memory = "Memory used: " + str(psutil.Process(os.getpid()).memory_info().rss / (1024 *1024  )) + " MB"
    performancetxt.write(" %s\n " % processedtime)
    performancetxt.write(" %s " % memory)
    performancetxt.close()

    print("Process Completed Succesfully !!! ")
    # Program End ********************
except Exception as e:
    print("Exception::: ",e)
