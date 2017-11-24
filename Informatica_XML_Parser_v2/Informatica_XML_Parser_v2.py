#Anaconda 4.3.1
#Thomas Luizzi, WSODT, 5/5/2017
#Informatica XML Parser V2.1
#Cleaned up the regex: re.search(r'\$Source\sconnection\svalue\:\s(\w+\:\w+)', line)

import re
from xml.dom import minidom

def xmlparser(xml):
    """
    This function takes an Informatica XML file and prints out all of the connection objects and
    connection variables (if any) for each session, then it appends the unique connection objects
    to the bottom of the text file.
    Input: a .XML file in the current working directory with no spaces in its file name.
    Output: a .TXT file of the same .XML name (to the left of the .) in the current working directory.
    """
    xmldoc = minidom.parse(xml)

    sessions = xmldoc.getElementsByTagName("SESSION")

    s_count = 0
    filename = str(xml).split('.')[0]

    file = open(filename + '.txt', 'w')

    for session in sessions:
        s_count += 1
        name = session.getAttribute("NAME")
        file.write(str(s_count)+ ": " + name + '\n')
        sessionextensions = session.getElementsByTagName("SESSIONEXTENSION")

        atts = session.getElementsByTagName("ATTRIBUTE")

        for att in atts:
            if att.attributes['NAME'].value == '$Source connection value':
                file.write('$Source connection value: ' + str(att.attributes['VALUE'].value) + '\n')

            if att.attributes['NAME'].value == '$Target connection value':
                file.write('$Target connection value: ' + str(att.attributes['VALUE'].value) + '\n')

        sesstransformationinists = session.getElementsByTagName("SESSTRANSFORMATIONINST")

        for sesstransformationinist in sesstransformationinists: #Finds Stored Procedures Connection Objects
            if sesstransformationinist.attributes['TRANSFORMATIONTYPE'].value == 'Stored Procedure':
                file.write('\t' + str(sesstransformationinist.attributes['SINSTANCENAME'].value) + '\n')
                file.write('\t\t SUBTYPE: ' + str(sesstransformationinist.attributes['TRANSFORMATIONTYPE'].value) + '\n')
                atts1 = sesstransformationinist.getElementsByTagName("ATTRIBUTE")
                for att in atts1:
                    file.write('\t\t CONNECTIONNAME: ' + str(att.attributes['VALUE'].value) + '\n')

        for sessionextension in sessionextensions:
             if sessionextension.attributes['TRANSFORMATIONTYPE'].value != 'Source Definition': #Removes the redundant Soure Definition
                 sinstancename = sessionextension.getAttribute('SINSTANCENAME')
                 file.write('\t' + sinstancename + '\n')
                 subtype = sessionextension.getAttribute('SUBTYPE')
                 file.write('\t\t SUBTYPE: ' + subtype + '\n')
                 connectionreferences = sessionextension.getElementsByTagName("CONNECTIONREFERENCE")

                 for connectionreference in connectionreferences:
                     file.write("\t\t CONNECTIONNAME: " + str(connectionreference.attributes['CONNECTIONNAME'].value) + '\n')
                     file.write("\t\t VARIABLE: " + str(connectionreference.attributes['VARIABLE'].value) + '\n')
        file.write('-' * 73 + '\n')
    if s_count == 1:
        file.write("There is only " + str(s_count) + " session.\n")
        file.write('-' * 73 + '\n')
    else:
        file.write("There are " + str(s_count) + " sessions.\n")
        file.write('-' * 73 + '\n')

    file.close()

    file = open(filename + '.txt', 'r') #Opens the .txt file to read.

    sources = []
    targets = []
    connections = []
    #variables = []

    #Create Regexes and append matches to lists 
    for line in file.readlines():
        s = re.search(r'\$Source\sconnection\svalue\:\s(\w+\:\w+)', line)
        if s != None: #Cannot use group method on None objects.
            sources.append(s.group(1))

        t = re.search(r'\$Target\sconnection\svalue\:\s(\w+\:\w+)', line)
        if t != None:
            targets.append(t.group(1))

        c = re.search(r'CONNECTIONNAME\:\s(\w+)', line)
        if c != None:
            connections.append(c.group(1))
    
    sources = list(set(sources))
    sources.sort()
    targets = list(set(targets))
    targets.sort()
    connections = list(set(connections))
    connections.sort()

    file.close()

    #Writes distinct sets of sources and targets

    file = open(filename + '.txt', 'a') #Append distinct connection objects to the bottom of the .txt file.
    file.write("Distinct $Source Connection Names:\n")
    file.write("\t" + "\n\t".join(sources) + "\n")
    file.write('-' * 105 + '\n')
    file.write("Distinct $Target Connection Names:\n")
    file.write("\t" + "\n\t".join(targets) + "\n")
    file.write('-' * 105 + '\n')
    file.write("Distinct Connection Names:\n")
    file.write("\t" + "\n\t".join(connections) + "\n")
    file.write('-' * 105)
    #file.write("Distinct Variable Names:\n")
    #file.write("\t" + "\n\t".join(set(variables)) + "\n")

    file.close()

xmlparser('LoadTDOTrafficDataMart_ADC.XML')

#for filename in os.listdir('C:\\Users\\luizzit\\Desktop'):
#	if filename.endswith('.XML'):
#		print(filename)