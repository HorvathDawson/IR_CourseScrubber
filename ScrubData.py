
from simplified_scrapy import SimplifiedDoc,req,utils,SimplifiedMain
import csv
url = 'https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments'
html = req.get(url)
departments = SimplifiedDoc(html).select('table').selects('a')
# # Get links
# all departments in a list
department_split = [department.html for department in departments]
# print(coursessplit)

print('done scrubbing for each department')
# find all courses in each department
allCourses = {}
for department in department_split:
    url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&sessyr=2020&sesscd=W&dept='+department+'&pname=subjarea'
    html = req.get(url)
    courses = SimplifiedDoc(html).select('table').selects('a')
    # all courses in a department
    courses_split = [course.html.split()[1] for course in courses]
    allCourses[department] = courses_split

print('done scrubbing for courses in each department')
print('building csv file of all availble course in UBC Winter 2020 ')
# department = 'APSC'
# courses = ['100', '101']
with open('allCourses.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for department, courses in allCourses.items():
        print('currently at the department: ' + department)
        for course in courses:
            url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course=' + course + '&sessyr=2020&sesscd=W&dept=' + department +'&pname=subjarea'
            html = req.get(url)
            sections = SimplifiedDoc(html).getElementsByTag('tr')
            # allSections = [section.selects('a|td>text()') for section in sections]
            # write to csv file
            for section in sections:
                row = section.selects('a|td>text()')
                if len(row) > 7:
                    spamwriter.writerow([row[0], row[1], row[2], row[3], row[5], row[6], row[7]])
