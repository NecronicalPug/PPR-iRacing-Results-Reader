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
            everything = []
            resultsdata = sessionresultsdata[y]["results"] #Reading actual sessions results out of session_results
            workaround = [] #Having to use a workaround to write a single word to the array.
            workaround.append(numberofsessions[y])
            header = ["Position","Name","Car Number","Car","Interval","Fastest Lap","Average Laps","Laps Completed"] #Header above all rows.

            with open("results.csv","a", newline = "") as file2: #Opening CSV file to write session state and header row.
                writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                writer.writerow(workaround)
                writer.writerow(header)

            for i in range(number): #Looping for each driver to read their data.
                temparray = []
                name = resultsdata[i]["display_name"]
                position = resultsdata[i]["finish_position"];position += 1
                lapscomplete = resultsdata[i]["laps_complete"]
                averagelap = resultsdata[i]["average_lap"];averagelap = find_lap(averagelap)
                bestlap = resultsdata[i]["best_lap_time"];bestlap = find_lap(bestlap)
                carid = resultsdata[i]["car_id"];carname = carids(carid)
                carnumber = resultsdata[i]["livery"]["car_number"]
                interval = resultsdata[i]["interval"];intervalresult = find_interval(interval)
                temparray.append(position);temparray.append(name);temparray.append(carnumber);temparray.append(carname);temparray.append(intervalresult);temparray.append(bestlap);temparray.append(averagelap);temparray.append(lapscomplete) #Appending to temporary array.
                everything.append(temparray)

                    



            with open("results.csv","a", newline = "") as file2: #Opening CSV file
                writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                writer.writerows(everything) #Writing each driver's data on a new row every time.
                 

                    

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


def find_interval(number): #Used to determine what the interval will be like, sucks that it's so complicated.
    number = str(number)
    if len(number) == 4:
        seconds = 0;milliseconds = number[0:3];result = (f'{seconds}.{milliseconds}')
        return result
    elif len(number) == 5:
        seconds = number[0];milliseconds = number[1:4];result = (f'{seconds}.{milliseconds}')
        return result
    elif len(number) == 6: #This is far more complicated than I'd like, but that's what happens when you cross over pure seconds.milliseconds and minutes.seconds.milliseconds.
        seconds = int(number[0:2]);milliseconds = number[2:5]
        if seconds < 60:
            result = (f'{seconds}.{milliseconds}')
            return result
        else: #Adding minutes.
            minutes = int(number[0:2]) // 60;seconds = int(number[0:2]) % 60
            if seconds < 10:
                seconds = str(f'0{seconds}')
            result = str(f'{minutes}:{seconds}.{milliseconds}')
            return result
    elif len(number) == 7:
        minutes = int(number[0:3]) // 60;seconds = int(number[0:3]) % 60;milliseconds = number[3:6]
        if seconds < 10: 
            seconds = str(f'0{seconds}') 
        result = str(f'{minutes}:{seconds}.{milliseconds}')
    elif int(number) <= 0:
        if int(number) == 0:
            return "Leader"
        elif int(number) < 0:
            return (f'{number} laps')
    else:
        return "Error"

def find_lap(number):
    number = str(number)
    try:
        if len(number) == 6:
            minutes = int(number[0:2]) // 60;seconds = int(number[0:2]) % 60;milliseconds = int(number[2:5]);result = (f'{seconds}.{milliseconds}')
            if seconds < 10:
                seconds = str(f'0{seconds}')
            result = str(f'{minutes}:{seconds}.{milliseconds}')
            return result
        elif len(number) == 7:
            minutes = int(number[0:3]) // 60;seconds = int(number[0:3]) % 60;milliseconds = number[3:6]
            if seconds < 10:
                seconds = str(f'0{seconds}')
            result = str(f'{minutes}:{seconds}.{milliseconds}')
            return result
        else:
            return "Error"
    except Exception:
        return "Error"


number = e.integerbox("Enter the number of drivers in the session.", "PPR iRacing Results Reader")
read_results(number)
