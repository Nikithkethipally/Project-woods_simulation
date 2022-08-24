# this program is to calculate the average, min and highest steps of each map stimulation
import sys

def selector(file1, file2, file3, file4, file5):
    """
    :param file1: file1
    :param file2: file2
    :param file3: file3
    :param file4: file4
    :param file5: file5
    :return: a selected file
    """

    print("Enter 1 for 300 map results")
    print("Enter 2 for 500 map results")
    print("Enter 3 for hard map results")
    print("Enter 4 for hell map results")
    print("Enter 5 for customized map results")
    option = input("Which results you want to analyze:\n ")

    while True:
        if option not in ["1", "2", "3", "4", "5", "6"]:
            print("Option not valid, re-enter your option")
            option = input("Which results you want to analyze:\n ")

        if option == "1":
            file = file1
            break
        elif option == "2":
            file = file2
            break
        if option == "3":
            file = file3
            break
        if option == "4":
            file = file4
            break
        if option == "5":
            file = file5
            break
    return file

def dataSorter(dataList):
    """
    :param dataList: A list with step counter
    :return: NONE
    """
    print("Your highest steps: " + str(max(dataList)))
    print("Your lowest steps: " + str(min(dataList)))
    print("Your average steps: " + str(sum(dataList) / len(dataList)))

def returnData():
    """
    Print categorized sorted data
    :return: None
    """
    file1 = "results/300results.txt"
    file2 = "results/500results.txt"
    file3 = "results/hardresults.txt"
    file4 = "results/hellresults.txt"
    file5 = "results/randomMap.txt"
    file = selector(file1, file2, file3, file4, file5)
    counter = 0
    player2_dataList = []
    player3_dataList = []
    player4_dataList = []

    with open(file, "r") as r:
        content = r.readlines()
        for line in content:
            counter += 1
            dataLine = line.split(" ")
            if dataLine[2] == "two":
                player2_dataList.append(int(dataLine[0]))
            if dataLine[2] == "three":
                player3_dataList.append(int(dataLine[0]))
            if dataLine[2] == "four":
                player4_dataList.append(int(dataLine[0]))

        if len(player2_dataList) > 0:
            print("For Player 2:")
            dataSorter(player2_dataList)
        if len(player3_dataList) > 0:
            print("For Player 3:")
            dataSorter(player3_dataList)
        if len(player4_dataList) > 0:
            print("For Player 4:")
            dataSorter(player3_dataList)

    anotherSearch = input("Want start another search? 'y' for yes, 'any key' for no")
    if anotherSearch in ["y", "yes", "Y", "YES", "Yes"]:
        returnData()
    else:
        print("Thanks for using data analyser")

    if counter == 0:
        print("Oops, your data is empty, want try another file?")
        returnData()

def stimulationData():
    """
    print Stimulation sorted data
    :return: None
    """
    # map step player
    file = "random.txt"
    map300_player2_dataList = []
    map300_player3_dataList = []
    map300_player4_dataList = []
    map500_player2_dataList = []
    map500_player3_dataList = []
    map500_player4_dataList = []
    map1000_player2_dataList = []
    map1000_player3_dataList = []
    map1000_player4_dataList = []
    with open(file, "r") as r:
        content = r.readlines()
        for line in content:
            dataLine = line.split(" ")
            if dataLine[0] == "300":
                if dataLine[2] == "2players\n":
                    map300_player2_dataList.append(int(dataLine[1]))
                if dataLine[2] == "3players\n":
                    map300_player3_dataList.append(int(dataLine[1]))
                if dataLine[2] == "4players\n":
                    map300_player4_dataList.append(int(dataLine[1]))
            if dataLine[0] == "500":
                if dataLine[2] == "2players\n":
                    map500_player2_dataList.append(int(dataLine[1]))
                if dataLine[2] == "3players\n":
                    map500_player3_dataList.append(int(dataLine[1]))
                if dataLine[2] == "4players\n":
                    map500_player4_dataList.append(int(dataLine[1]))
            if dataLine[0] == "1000":
                if dataLine[2] == "2players\n":
                    map1000_player2_dataList.append(int(dataLine[1]))
                if dataLine[2] == "3players\n":
                    map1000_player3_dataList.append(int(dataLine[1]))
                if dataLine[2] == "4players\n":
                    map1000_player4_dataList.append(int(dataLine[1]))

        if len(map300_player2_dataList) > 0:
            print("For map 300*300 and 2player:")
            dataSorter(map300_player2_dataList)
        if len(map300_player3_dataList) > 0:
            print("For map 300*300 and 3player:")
            dataSorter(map300_player2_dataList)
        if len(map300_player4_dataList) > 0:
            print("For map 300*300 and 4player:")
            dataSorter(map300_player2_dataList)

        if len(map500_player2_dataList) > 0:
            print("For map 500*500 and 2 player:")
            dataSorter(map500_player2_dataList)
        if len(map500_player3_dataList) > 0:
            print("For map 500*500 and 3 player:")
            dataSorter(map500_player2_dataList)
        if len(map500_player4_dataList) > 0:
            print("For map 500*500 and 4 player:")
            dataSorter(map500_player2_dataList)

        if len(map1000_player2_dataList) > 0:
            print("For map 1000*1000 and 2 player:")
            dataSorter(map500_player2_dataList)
        if len(map1000_player3_dataList) > 0:
            print("For map 1000*1000 and 3 player:")
            dataSorter(map500_player2_dataList)
        if len(map1000_player4_dataList) > 0:
            print("For map 1000*1000 and 4 player:")
            dataSorter(map1000_player2_dataList)

def Menu():
    """
    Menu page
    :return: None
    """
    option = input("Enter 1 to view stimulation data, 2 to view manual input data, 3 to exit menu\t")
    while True:
        if option == "3":
            sys.exit()
        if option in ["1", "2"]:
            if option == "1":
                stimulationData()
                Menu()
            if option == "2":
                returnData()
                Menu()
        else:
            option = input("Enter 1 to view stimulation data, 2 to view manual input data, 3 to exit menu\t")

Menu()
