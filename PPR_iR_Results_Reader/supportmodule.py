import sys
import timeit #Execution time measuring
import json #Json reader
import csv #CSV file operations
import time #Slowing code down.


def read_results(number,racesessionnumber):
    
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
            header = ["Position","Name","Car Number","Car","Interval","Fastest Lap","Laps Completed","Points"] #Header above all rows.

            with open("results.csv","a", newline = "") as file2: #Opening CSV file to write session state and header row.
                writer = csv.writer(file2, delimiter = ";") #CSV writer module. 
                writer.writerow(workaround)
                writer.writerow(header)
            
            propositioninclassiterator = 0  #Way to get the positions working.
            ampositioninclassiterator = 0 
            for i in range(number): #Looping for each driver to read their data.
                temparray = []
                name = resultsdata[i]["display_name"]
                position = resultsdata[i]["finish_position"];position += 1
                lapscomplete = resultsdata[i]["laps_complete"]
                try: #Same thing as bestlap
                    averagelap = resultsdata[i]["average_lap"];averagelap = str(averagelap);minutes = int(averagelap[0:3]) // 60;milliseconds = averagelap[3:6] #Converting a weird average lap into a readable laptime.
                    seconds = int(averagelap[0:3]) % 60
                    if seconds < 10: #Preventing a missing 0 from occurring. 
                        seconds = str(f'0{seconds}') 
                    averagelap = str(f'{minutes}:{seconds}.{milliseconds}')
                except ValueError:
                    averagelap = "None" 
                try:
                    bestlap = resultsdata[i]["best_lap_time"];bestlap = str(bestlap);minutes = int(bestlap[0:3]) // 60;milliseconds = bestlap[3:6] #Converting a weird best lap into a readable laptime.
                    seconds = int(bestlap[0:3]) % 60
                    if seconds < 10: 
                        seconds = str(f'0{seconds}') 
                    bestlap = str(f'{minutes}:{seconds}.{milliseconds}')
                except ValueError: #No errors in these ends.
                    bestlap = "None"
                carid = resultsdata[i]["car_id"];carname = carids(carid)
                carnumber = resultsdata[i]["livery"]["car_number"]
                if int(carnumber) // 100 == 1:
                    classname = "Am"
                    ampositioninclassiterator += 1
                else:
                    classname = "Pro"
                    propositioninclassiterator += 1
                interval = resultsdata[i]["interval"];print(interval);intervalresult = find_interval(interval)
                if sessionresultsdata[y]["simsession_name"] == "RACE":
                    if classname == "Am":
                        points = get_points(ampositioninclassiterator,racesessionnumber)
                    else:
                        points = get_points(propositioninclassiterator,racesessionnumber)
                else:
                    points = ""
                temparray.append(position);temparray.append(name);temparray.append(carnumber);temparray.append(carname);temparray.append(intervalresult);temparray.append(bestlap);temparray.append(lapscomplete);temparray.append(points);temparray.append(classname); #Appending to temporary array.       
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


def get_points(position,racesessionnumber): #Calculating championship points based on position.
    if racesessionnumber == 1:
        divider = 1
    elif racesessionnumber == 2:
        divider = 2
    else:
        print("Error.")

    if position ==  1:
        points = 30 / divider
        return points
    elif position ==  2:
        points = 25 / divider
        return points
    elif position ==  3:
        points = 21 / divider
        return points    
    elif position ==  4:
        points = 18 / divider
        return points
    elif position ==  5:
        points = 16 / divider
        return points
    elif position ==  6:
        points = 14 / divider
        return points
    elif position ==  7:
        points = 12 / divider
        return points
    elif position ==  8:
        points = 11 / divider
        return points
    elif position ==  9:
        points = 10 / divider
        return points    
    elif position ==  10:
        points = 9 / divider
        return points
    elif position ==  11:
        points = 8 / divider
        return points
    elif position ==  12:
        points = 7 / divider
        return points
    elif position ==  13:
        points = 6 / divider
        return points
    elif position ==  14:
        points = 5 / divider
        return points
    elif position ==  15:
        points = 4 / divider
        return points    
    elif position ==  16:
        points = 3 / divider
        return points
    elif position ==  17:
        points = 2 / divider
        return points
    elif position ==  18:
        points = 1 / divider
        return points
    elif position >= 19:
        points = 0
        return points