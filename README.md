# invoiceManager
* A python-based application for managing projects and billing.
![image](https://user-images.githubusercontent.com/74081885/210866594-e06919a3-ae50-4406-9671-3d2b6432b42d.png)
## Application Features
* Add any number of Projects with it's name, address, start date, client name and info, project type (Hourly or Flat Fee), Activities (Work related to project i.e. employee hours spent on drafting), and billing (Balance, invoices, remaining balance).
* Data is stored as a JSON file (Can easily be used by other programs). 
  * Example JSON:
  ```
  {
  "Hollywood": 
      {"date": "01/01/2023", "address": "123 Hollywood Ave", "payment": 0, "balance": 6700, "client": {"name": "Bob John", "address": "321 Broadway Ave", "number": "888-888-8888", "email": "BobJohn@gmail.com"}, "description": "", "activities": [["01/03/2023", "Joe", "7", "Design of Building"], ["01/02/2023", "Ron", "4", "Drafting Building Drawing"]], "type": "Hourly"}
  }
   ```
* Sophisticated project search: Searching for a project considers many characteristics of a project (i.e. project name, project date, client name, balance etc.)
