import supportmodule as s #Contains the functions
import easygui as e #GUI Element

number = e.integerbox("Enter the number of drivers in the session. ","iRacing Results Reader")
number2 = e.integerbox("1 race/2 races (1/2)","iRacing Results Reader")
s.read_results(number,number2)