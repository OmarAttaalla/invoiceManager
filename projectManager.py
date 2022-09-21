class projectManager(object):
    def __init__(self):
        self.projectNames = []
        self.projects = {}
    def renderProject(self, projectObject, window):
        window["projectName"].update(projectObject.name)
        window["projectAddress"].update("Address: " + projectObject.address)
        window["projectDate"].update("Date: " + projectObject.date)
        window["clientName"].update("Client: " + projectObject.client)
        window["projectBalance"].update("Balance: $" + str(projectObject.balance))
        window["projectPayment"].update("Paid: $" + str(projectObject.payment))
        window["projectRemainingBalance"].update("Remaining Balance: $" + str(projectObject.remainingBalance))
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