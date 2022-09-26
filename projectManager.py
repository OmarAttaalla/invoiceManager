import json
import os

def JSON_ENCODE_PROJECTS(dict):
    new_dict = {}
    for key in dict:
        new_dict[key] = {
            "date": dict[key].date,
            "address": dict[key].address,
            "payment": dict[key].payment,
            "balance": dict[key].balance,
            "client": dict[key].client,
            "description": dict[key].description,
            "activities": dict[key].render_activities(),
            "type": dict[key].type
        }


    return new_dict

class projectManager(object):
    def __init__(self):
        self.projectNames = []
        self.projects = {}
    def renderProject(self, projectObject, window):
        window["projectName"].update(projectObject.name)
        window["projectAddress"].update("Address: " + projectObject.address)
        window["projectDate"].update("Project Start: " + projectObject.date)
        window["clientName"].update("Client: " + projectObject.client["name"])
        window["clientNumber"].update("     number: " + projectObject.client["number"])
        window["clientAddress"].update("     address: " + projectObject.client["address"])
        window["clientEmail"].update("     email: " + projectObject.client["email"])
        window["projectType"].update("Project Type: " + projectObject.type)
        window["projectBalance"].update("Balance: $" + str(projectObject.balance))
        window["projectPayment"].update("Paid: $" + str(projectObject.payment))
        window["projectRemainingBalance"].update("Remaining Balance: $" + str(projectObject.remainingBalance))
        window["activitiesTable"].update(values=projectObject.render_activities())
        if projectObject.remainingBalance > 0:
            window["projectRemainingBalance"].update(text_color="red")
        else:
            window["projectRemainingBalance"].update(text_color="green")
    def filterProjects(self, text):
        filtered_projects = []
        for name in self.projectNames:
            if name.lower().find(text.lower()) != -1:
                filtered_projects.append(name)
            elif self.projects[name].date.lower().find(text.lower()) != -1:
                filtered_projects.append(name)
            elif self.projects[name].address.lower().find(text.lower()) != -1:
                filtered_projects.append(name)
        return filtered_projects
    def saveProjects(self): #Stores Projects in a JSON File
        jsonObj = json.dumps(JSON_ENCODE_PROJECTS(self.projects))
        jsonFile = open("Projects.json", "w")
        jsonFile.write(jsonObj)
        jsonFile.close()