import easygui as e #GUI element
import sys
import timeit #Execution time measuring
import json #Json reader
import csv #CSV file operations
import time #Slowing code down.


def read_results(number):
    
    file = open("results.csv","w") #Opening file where results will be saved.
    file.write("")
    file.close()
 
    with open("results.json") as file: #Opening file
        data = json.load(file)
        sessionresultsdata = data["session_results"] #Reading just the session_results out of everything
        numberofsessions = []
        for i in sessionresultsdata:
            numberofsessions.append(i["simsession_name"])
        totaliterations = len(numberofsessions)
        for y in range(totaliterations):
            resultsdata = sessionresultsdata[y]["results"] #Reading actual sessions results out of session_results
            workaround = [] #Having to use a workaround to write a single word to the 
            workaround.append(numberofsessions[y])
            header = ["Position","Name","Car Number","Car","Fastest Lap","Laps Completed"] #Header above all rows.

            with open("results.csv","a", newline = "") as file2: #Opening CSV file to write session state and header row.
                writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                writer.writerow(workaround)
                writer.writerow(header)

            for i in range(number): #Looping for each driver to read their data.
                temparray = []
                name = resultsdata[i]["display_name"]
                position = resultsdata[i]["finish_position"];position += 1
                lapscomplete = resultsdata[i]["laps_complete"]
                try:
                    bestlap = resultsdata[i]["best_lap_time"];bestlap = str(bestlap);minutes = int(bestlap[0:3]) // 60;milliseconds = bestlap[3:6] #Converting a weird best lap into a readable laptime.
                    seconds = int(bestlap[0:3]) % 60
                    if seconds < 10: #Preventing a missing 0 from occurring. 
                        seconds = str(f'0{seconds}') 
                    bestlap = str(f'{minutes}:{seconds}.{milliseconds}')
                except ValueError: #No errors in these ends.
                    bestlap = "None"
                carid = resultsdata[i]["car_id"];carname = carids(carid)
                carnumber = resultsdata[i]["livery"]["car_number"]
                temparray.append(position);temparray.append(name);temparray.append(carnumber);temparray.append(carname);temparray.append(bestlap);temparray.append(lapscomplete) #Appending to temporary array.
                print(temparray)
            
            
                with open("results.csv","a", newline = "") as file2: #Opening CSV file
                    writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                    writer.writerow(temparray) #Writing each driver's data on a new row every time.

                    

    print("Process Complete")
    time.sleep(2)
    sys.exit()

def carids(carid): #Function to find the car make assigned to car ids in iracing.
    if carid == 43:
        return("Mclaren MP4-12C")
    elif carid == 59:
        return("Ford GT3")
    elif carid == 72:
        return("Mercedes AMG")
    elif carid == 73:
        return("Audi R8 LMS")
    elif carid == 94:
        return("Ferrari 488")
    elif carid == 132:
        return("BMW M4 Prototype")
    elif carid == 133:
        return("Lamborghini Huracan Evo")
    else:
        return("Error")

number = e.integerbox("Enter the number of drivers in the session.", "PPR iRacing Results Reader")
read_results(number)
