import easygui as e #GUI element
import sys
import timeit #Execution time measuring
import json #Json reader
import csv #CSV file operations

def read_results(number):
    start = timeit.timeit() #Starting Timer
    
    file = open("results.csv","w");file.write("");file.close() #Opening file where results will be saved.
 
    with open("results.json") as file: #Opening file
        data = json.load(file)
        sessionresultsdata = data["session_results"] #Reading just the session_results out of everything
        resultsdata = sessionresultsdata[0]["results"] #Reading actual sessions results out of session_results

        for i in range(number): #Looping for each driver to read their data.
            temparray = []
            name = resultsdata[i]["display_name"]
            position = resultsdata[i]["finish_position"];position += 1
            lapscomplete = resultsdata[i]["laps_complete"]
            bestlap = resultsdata[i]["best_lap_time"];bestlap = str(bestlap);minutes = int(bestlap[0:3]) // 60;seconds = int(bestlap[0:3]) % 60;milliseconds = int(bestlap[4:]);bestlap = str(f'{minutes}:{seconds}.{milliseconds}') #Converting a weird best lap into a readable laptime.
            carnumber = resultsdata[i]["livery"]["car_number"]
            temparray.append(position);temparray.append(name);temparray.append(carnumber);temparray.append(bestlap);temparray.append(lapscomplete) #Appending to temporary array.
            print(temparray)
            
            
            with open("results.csv","a", newline = "") as file2: #Opening CSV file
                writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                writer.writerow(temparray) #Writing each driver's data on a new row every time.

    end = timeit.timeit()
    print(f'Process completed in {end - start} seconds.')

number = e.integerbox("Enter the number of drivers in the session.", "PPR iRacing Results Reader")
read_results(number)
