from turtle import color
from xml.etree.ElementTree import TreeBuilder
import PySimpleGUI as sg
import os
from project import project
from projectManager import projectManager
import json


font = ('Oswald', 12)
sg.theme('Reddit')
sg.set_options(font=font)

projectManagerObj = projectManager()

project_column = sg.Column(
    [
        [sg.Text('Projects')], [sg.Button("+", key="addProject", size=(2,1)), sg.InputText("", size=(12,5), key="searchProject", enable_events=True)], [sg.Listbox(values=projectManagerObj.projectNames, size=(15,40), key="Project", enable_events=True)]
    ]
)

activities_header = ["date", "employee", "hours", "description"]
billing_header =["invoice", "date", "ID"]

project_detail = sg.Column(
    [ 
        [sg.Frame("Project", [
                [sg.Text("Address: Select a Project", key="projectAddress")], 
                [sg.Text("Project Start: Select a Project", key="projectDate")],
                [sg.Text("Client: Select a Project", key="clientName")],
                [sg.Text("     address: select a project", font=('Oswald', 10), key="clientAddress")],
                [sg.Text("     number: select a project", font=('Oswald', 10), key="clientNumber")],
                [sg.Text("     email: select a project", font=('Oswald', 10), key="clientEmail")],
                [sg.Text("Project Type: Select a Project", key="projectType")],
            ]
        , key="projectName", size=(500,225))],
        [sg.Frame("Activities", [
                [sg.Table(values=[], headings=activities_header, max_col_width=35, auto_size_columns= False, key="activitiesTable", justification="c", enable_events=True, expand_x=True)],
                [sg.Button("Add", key="addActivity")]
            ]
        , size=(500,275))],
        [sg.Frame("Billing", [
                [sg.Text("Balance: Select a Project", key="projectBalance", text_color="gray")],
                [sg.Text("Paid: Select a Project", key="projectPayment", text_color="green")], 
                [sg.Text("Remaining Balance: Select a Project", key="projectRemainingBalance")],
                [sg.Table(values=[], headings=billing_header, auto_size_columns= False, key="billingTable", justification="c", enable_events=True, expand_x=True)]
            ]
        , size=(500,300))]
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

def JSON_DECODE_PROJECTS(dict):
    new_dict = {}
    for key in dict:
        new_dict[key] = project(key, dict[key]["date"], dict[key]["address"], dict[key]["payment"], dict[key]["balance"], dict[key]["client"], dict[key]["description"], dict[key]["type"]) #Create Project Object
        for act in dict[key]["activities"]:
            new_dict[key].add_activity(act[0], act[1], act[2], act[3])
        projectManagerObj.projectNames.append(key)
    return new_dict


def display_note(dict, title): #Takes in a dictionary of title, value pairs and displays it in a new window
    newLayout = []

    for key in dict:
        newLayout.append([sg.Text(key, font=("Oswald", 12, "bold")), sg.Text(dict[key])])

    newWindow = sg.Window(title, newLayout)
    while True:
        event, values = newWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    newWindow.close()

def addProject(): #Opens window to add a new project
    newLayout = [
        [sg.Text("Project Name: "), sg.In("", key="setProjectName", expand_x=True)],
        [sg.Text("Project Address: "), sg.In("", key="setProjectAddress", expand_x=True)],
        [sg.Text("Client Name: "), sg.In("", key="setClientName", expand_x=True)],
        [sg.Text("Client Address: "), sg.In("", key="setClientAddress", expand_x=True)],
        [sg.Text("Client Number: "), sg.In("", key="setClientNumber", expand_x=True)],
        [sg.Text("Client Email: "), sg.In("", key="setClientEmail", expand_x=True)],
        [sg.Text("Project Type: "), sg.Radio("Hourly", "projectType", key="HourlyType"), sg.Radio("Flat Fee", "projectType", key="flatFeeType")],
        [sg.Text("Project Start: "), sg.In("", key="setProjectDate"), sg.CalendarButton("Select Date", format='%m/%d/%Y')],
        [sg.Text("Balance: "), sg.In("", key="setProjectBalance", expand_x=True)],
        [sg.Button("Add Project", key="confirmAddProject"), sg.Text("", text_color="red", key="errorAddProj")]
    ]
    newWindow = sg.Window("Add Project", newLayout)
    while True:
        event, values = newWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "confirmAddProject":
            if values["setProjectName"] == "":
                newWindow["errorAddProj"].update("Project must have a Project Name")
            elif values["setProjectName"] in projectManagerObj.projectNames:
                newWindow["errorAddProj"].update("Project Name Already Exists")
            elif values["setProjectBalance"].isdigit() == False:
                newWindow["errorAddProj"].update("Balance must be a valid numeric value")
            else:
                clientInfo = {
                    "name": values["setClientName"],
                    "address": values["setClientAddress"],
                    "number": values["setClientNumber"],
                    "email": values["setClientEmail"] 
                }
                project_type = "Hourly"
                if (values["HourlyType"] == False):
                    project_type = "Flat Fee"
                newProject = project(values["setProjectName"], values["setProjectDate"], values["setProjectAddress"], 0, int(values["setProjectBalance"]), clientInfo, "", project_type)
                projectManagerObj.projectNames.append(newProject.name)
                projectManagerObj.projects[newProject.name] = newProject
                window["Project"].update(values=projectManagerObj.projectNames)
                
                #Store Projects as JSON File
                projectManagerObj.saveProjects()
                break
    newWindow.close()

def addActivity(): #Opens window to add a new project
    newLayout = [
        [sg.Text("Employee: "), sg.In("", key="setActivityEmployee")],
        [sg.Text("Date: "), sg.In("", key="setActivityDate"), sg.CalendarButton("Select Date", format='%m/%d/%Y')],
        [sg.Text("Hours: "), sg.In("", key="setActivityHours")],
        [sg.Text("Description: "), sg.In("", key="setActivityDescription")],
        [sg.Button("Add Activity", key="confirmAddActivity"), sg.Text("", text_color="red", key="errorAddActivity")]
    ]
    newWindow = sg.Window("Add Activity", newLayout)
    while True:
        event, newValues = newWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "confirmAddActivity":
            if newValues["setActivityEmployee"] == "":
                newWindow["errorAddActivity"].update("Employee Name Required")
            elif newValues["setActivityHours"].isdigit() == False:
                newWindow["errorAddActivity"].update("Hours must be a valid numeric value")
            elif values["Project"] != None and len(values["Project"]) > 0:
                projectObject = projectManagerObj.projects[values["Project"][0]]
                projectObject.add_activity(newValues["setActivityDate"], newValues["setActivityEmployee"], newValues["setActivityHours"], newValues["setActivityDescription"])
                window["activitiesTable"].update(values=projectObject.render_activities())
                projectManagerObj.saveProjects()
                break
    newWindow.close()
 

if os.path.exists("Projects.json"):
    f = open("Projects.json")
    data = json.load(f)
    projectManagerObj.projects = JSON_DECODE_PROJECTS(data)

searchText = "" #Used to filter Projects

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values["Project"] != None and len(values["Project"]) > 0:
        projectObject = projectManagerObj.projects[values["Project"][0]]
        projectManagerObj.renderProject(projectObject, window)
    if event == "addProject":
        addProject()
    if values["searchProject"] != searchText:
        searchText = values["searchProject"]
        window["Project"].update(values=projectManagerObj.filterProjects(searchText))
    if event == "addActivity" and values["Project"] != None and len(values["Project"]) > 0:
        addActivity()
    if event == "activitiesTable" and values["Project"] != None and len(values["Project"]) > 0:
        if len(values["activitiesTable"]) > 0:
            projectObject = projectManagerObj.projects[values["Project"][0]]
            activityDict = {
                "date:": projectObject.activities[values["activitiesTable"][0]].date,
                "employee:": projectObject.activities[values["activitiesTable"][0]].employee,
                "hours:": projectObject.activities[values["activitiesTable"][0]].hours,
                "description:": projectObject.activities[values["activitiesTable"][0]].description
            }

            display_note(activityDict, "Activity")

    
window.close()