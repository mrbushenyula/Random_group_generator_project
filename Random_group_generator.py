
class LecturerTask:
    name=None
    def __init__(self,name):
        self.name=name
    def ClassGroups (self,MainList):
        pass
    
class RandomGroupsIT(LecturerTask):
    name = None

    def __init__(self, name):
        self.name = name

    def ClassGroups(self, MainList):
        import random as rd  # Import random module locally within the method

        thelist = []

        while True:
            self.name = input("add name: ")
            MainList.append(self.name)
            addStudent = input("add another student?(yes or no): ")
            if addStudent == "yes":
                continue
            elif addStudent == "no":
                break

        for element in MainList:
            thelist.append(element)

        GroupList = []  # append in this the different groups chosen from the main list

        if len(thelist) == 0:
            print("\nThere is no student registered yet\n")
        elif 1 <= len(thelist) <= 2:
            print("\n", thelist, "\n")
        else:
            print()
            print("INFORMATION TECHNOLOGY groups")
            print()
            group = []

            while True:
                for i in range(3):
                    element = rd.choice(thelist)
                    group.append(element)
                    thelist.remove(element)
                GroupList.append(group)
                print()
                for element in group:
                    print(element)
                print()
                group = []

                if len(thelist) < 3:
                    break
                else:
                    continue

class RandomGroupsCS(LecturerTask):
    name = None

    def __init__(self, name):
        self.name = name

    def ClassGroups(self, MainList):
        import random as rd  # Import random module locally within the method

        thelist = []

        while True:
            self.name = input("add name: ")
            MainList.append(self.name)
            addStudent = input("add another student?(yes or no): ")
            if addStudent == "yes":
                continue
            elif addStudent == "no":
                break

        for element in MainList:
            thelist.append(element)

        GroupList = []  # append in this the different groups chosen from the main list

        if len(thelist) == 0:
            print("\nThere is no student registered yet\n")
        elif 1 <= len(thelist) <= 2:
            print("\n", thelist, "\n")
        else:
            print()
            print("COMPUTER SCIENCE groups")
            print()
            group = []

            while True:
                for i in range(3):
                    element = rd.choice(thelist)
                    group.append(element)
                    thelist.remove(element)
                GroupList.append(group)
                print()
                for element in group:
                    print(element)
                print()
                group = []

                if len(thelist) < 3:
                    break
                else:
                    continue

class RandomGroupsDS(LecturerTask):
    name = None

    def __init__(self, name):
        self.name = name

    def ClassGroups(self, MainList):
        import random as rd  # Import random module locally within the method

        thelist = []

        while True:
            self.name = input("add name: ")
            MainList.append(self.name)
            addStudent = input("add another student?(yes or no): ")
            if addStudent == "yes":
                continue
            elif addStudent == "no":
                break

        for element in MainList:
            thelist.append(element)

        GroupList = []  # append in this the different groups chosen from the main list

        if len(thelist) == 0:
            print("\nThere is no student registered yet\n")
        elif 1 <= len(thelist) <= 2:
            print("\n", thelist, "\n")
        else:
            print()
            print("DATA SCIENCE groups")
            print()
            group = []

            while True:
                for i in range(3):
                    element = rd.choice(thelist)
                    group.append(element)
                    thelist.remove(element)
                GroupList.append(group)
                print()
                for element in group:
                    print(element)
                print()
                group = []

                if len(thelist) < 3:
                    break
                else:
                    continue



def ClassChoice():
    cho=input("what class is this (IT,CS,DS): ")
    
    if cho=="IT" or cho=="it" or cho=="It":
        print()
        GroupObject = RandomGroupsIT(None)
        GroupObject.ClassGroups([])
    elif cho=="CS" or cho=="cs" or cho=="Cs":
        print()
        GroupObject = RandomGroupsCS(None)
        GroupObject.ClassGroups([])
    elif cho=="DS" or cho=="ds" or cho=="Ds":
        print()
        GroupObject = RandomGroupsDS(None)
        GroupObject.ClassGroups([])
        

ClassChoice()



