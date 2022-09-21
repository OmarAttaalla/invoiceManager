from turtle import color
import PySimpleGUI as sg
import os
from project import project
import json


font = ('Oswald', 12)
sg.theme('Reddit')
sg.set_options(font=font)

projectNames= []
projects = {}

project_column = sg.Column(
    [
        [sg.Text('Projects')], [sg.Button("+", key="addProject", size=(2,1)), sg.InputText("", size=(12,5), key="searchProject", enable_events=True)], [sg.Listbox(values=projectNames, size=(15,20), key="Project", enable_events=True)]
    ]
)


project_detail = sg.Column(
    [ 
        [sg.Frame("Project", [
                [sg.Text("Address: Select a Project", key="projectAddress")], 
                [sg.Text("Date: Select a Project", key="projectDate")],
                [sg.Frame("Payments", [
                        [sg.Text("Balance: Select a Project", key="projectBalance", text_color="gray")],
                        [sg.Text("Paid: Select a Project", key="projectPayment", text_color="green")], 
                        [sg.Text("Remaining Balance: Select a Project", key="projectRemainingBalance")]
                    ]
                )]

            ]
        , key="projectName")]
    ]
)


file_list_column = [
    project_column,
    project_detail
]

layout = [
    [
        file_list_column,
    ]
]

window = sg.Window(title="Invoice Manager", layout=layout, margins=(0,0))

def JSON_ENCODE_PROJECTS(dict):
    new_dict = {}
    for key in dict:
        new_dict[key] = {
            "date": dict[key].date,
            "address": dict[key].address,
            "payment": dict[key].payment,
            "balance": dict[key].balance
        }
    return new_dict

def JSON_DECODE_PROJECTS(dict):
    new_dict = {}
    for key in dict:
        new_dict[key] = project(key, dict[key]["date"], dict[key]["address"], dict[key]["payment"], dict[key]["balance"]) #Create Project Object
        projectNames.append(key)
    return new_dict


def addProject(): #Opens window to add a new project
    newLayout = [
        [sg.Text("Project Name: "), sg.In("", key="setProjectName")],
        [sg.Text("Project Address: "), sg.In("", key="setProjectAddress")],
        [sg.Text("Project Date: "), sg.In("", key="setProjectDate"), sg.CalendarButton("Select Date", format='%m/%d/%Y', key="setProjectName")],
        [sg.Text("Balance: "), sg.In("", key="setProjectBalance")],
        [sg.Button("Add Project", key="confirmAddProject")]
    ]
    newWindow = sg.Window("Add Project", newLayout)
    while True:
        event, values = newWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "confirmAddProject":
            if values["setProjectName"] == "":
                print("Need Project Name")
            elif values["setProjectName"] in projectNames:
                print("Project Name Already Exists")
            else:
                newProject = project(values["setProjectName"], values["setProjectDate"], values["setProjectAddress"], 0, int(values["setProjectBalance"]))
                projectNames.append(newProject.name)
                projects[newProject.name] = newProject
                window["Project"].update(values=projectNames)
                
                #Store Projects as JSON File
                jsonObj = json.dumps(JSON_ENCODE_PROJECTS(projects))
                jsonFile = open("Projects.json", "w")
                jsonFile.write(jsonObj)
                jsonFile.close()
                break
    newWindow.close()

def filterProjects(text):
    filtered_projects = []
    for name in projectNames:
        if name.lower().find(text.lower()) != -1:
            filtered_projects.append(name)
        elif projects[name].date.lower().find(text.lower()) != -1:
            filtered_projects.append(name)
        elif projects[name].address.lower().find(text.lower()) != -1:
            filtered_projects.append(name)
    return filtered_projects


if os.path.exists("Projects.json"):
    f = open("Projects.json")
    data = json.load(f)
    projects = JSON_DECODE_PROJECTS(data)

searchText = "" #Used to filter Projects

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values["Project"] != None and len(values["Project"]) > 0:
        projectObject = projects[values["Project"][0]]
        window["projectName"].update(projectObject.name)
        window["projectAddress"].update("Address: " + projectObject.address)
        window["projectDate"].update("Date: " + projectObject.date)
        window["projectBalance"].update("Balance: $" + str(projectObject.balance))
        window["projectPayment"].update("Paid: $" + str(projectObject.payment))
        window["projectRemainingBalance"].update("Remaining Balance: $" + str(projectObject.remainingBalance))
        if projectObject.remainingBalance > 0:
            window["projectRemainingBalance"].update(text_color="red")
        else:
            window["projectRemainingBalance"].update(text_color="green")
    if event == "addProject":
        addProject()
    if values["searchProject"] != searchText:
        searchText = values["searchProject"]
        window["Project"].update(values=filterProjects(searchText))

    
window.close()