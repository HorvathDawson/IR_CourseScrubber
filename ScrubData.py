
from simplified_scrapy import SimplifiedDoc,req,utils,SimplifiedMain
import csv
import urllib.request

url = 'https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments'
try:
    html = req.get(url)
    # response = urllib.request.urlopen(url)
    # html = response.read()
except:
    print("failed to load anything... fuck me")

departments = SimplifiedDoc(html).select('table').selects('a')
# # Get links
# all departments in a list
departmentCodes = [department.html for department in departments]
# print(coursessplit)

print('done scrubbing for each department')
# find all courses in each department
# departmentCodes = ['APSC', 'COMR']
allCourses = {}
for department in departmentCodes:
    url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&sessyr=2020&sesscd=W&dept='+department+'&pname=subjarea'
    try:
        html = req.get(url)
        # response = urllib.request.urlopen(url)
        # html = response.read()
    except:
        print("failed to load department page for: " + department)

    courses = SimplifiedDoc(html).select('table').selects('a')
    # all courses in a department
    courses_split = [course.html.split()[1] for course in courses]
    allCourses[department] = courses_split

print('done scrubbing for courses in each department')
print('building csv file of all available course in UBC Winter 2020 ')

# allCourses = {
#     'APSC': ['100']
# }
with open('allCoursesWithDescription.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Status', 'Course Section', 'Title', 'Instructor','Activity', 'Term', 'Days', 'Start-End', 'Description', 'Comments', 'Course Url'])
    for department, courses in allCourses.items():
        print('currently at the department: ' + department)
        for course in courses:
            url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course=' + course + '&sessyr=2020&sesscd=W&dept='+ department +'&pname=subjarea'
            try:
                html = req.get(url)
                # response = urllib.request.urlopen(url)
                # html = response.read()
            except:
                print("error loading the course: " + course + " in the department: " + department)

            sections = SimplifiedDoc(html).getElementsByTag('tr')
            # allSections = [section.selects('a|td>text()') for section in sections]
            # write to csv file
            for section in sections:
                row = section.selects('a|td>text()')
                if len(row) > 7:
                    url = 'https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=' + department + '&course=' + course + '&section=' + row[1].split()[2]
                    try:
                        html = req.get(url)
                        # response = urllib.request.urlopen(url)
                        # html = response.read()
                    except:
                        print("error loading page for: ", row[1])

                    sectionPage = SimplifiedDoc(html)
                    # get the instructor name
                    tables = sectionPage.getElementsByTag('table')
                    instructor = [table.getElementByReg('<td>Instructor:*') for table in tables]

                    instructor = list(filter(None, instructor))
                    if len(instructor) > 0:
                        instructor = instructor[0]
                        instructor = instructor.selects('a|td>text()')
                    else:
                        instructor = ['','None Found']
                    # print(instructor)
                    # get title and description
                    title = sectionPage.getElementByClass('content expand').getElementByTag('h5').html
                    description = sectionPage.getElementByClass('content expand').getElementByTag('p').html
                    spamwriter.writerow([row[0], row[1], title, instructor[1], row[2], row[3], row[5], row[6]+'-'+row[7], description, row[8], url])
