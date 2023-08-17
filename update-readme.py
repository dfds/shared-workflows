#!/usr/bin/env python

import os
import yaml
import pathlib

# Line break
def lb():
    return "\n"

# Double line break
def dlb():
    return lb() + lb()

# Indentation
def ind():
    return "\t"

def rootReadmeHeader():
    headlineFile = open('headline.md')
    headlineContent = headlineFile.read()
    headlineFile.close()

    return headlineContent

examplesDir = 'examples'
headerReadmeContent = rootReadmeHeader()
bodyReadmeConetent = []
collection = {}

# Create example collection
for example in sorted(os.listdir(examplesDir)):
    examplePath = os.path.join(examplesDir, example)
    name = pathlib.Path(examplePath).stem
    workflowPath = os.path.join('.github/workflows', example)
    actionPath = os.path.join('.github/actions', name, 'action.yml')

    # Ignore folders here
    if os.path.isdir(examplePath):
        continue

    # Extract the category from filename
    category = example.split('-')[0]

    # Check if accompanied file exist
    if os.path.isfile(workflowPath):
        sharedType = 'workflows'
    elif os.path.isfile(actionPath):
        sharedType = 'actions'
    else:
        continue

    if not category in collection.keys():
        collection[category] = {}

    if not sharedType in collection[category].keys():
        collection[category][sharedType] = []
    
    collection[category][sharedType].append(examplePath)

for category in collection:
    # Insert the category list item in the README index
    headerReadmeContent += lb() + '- [' + category.title() + '](#' + category + ')'

    # Initialize the category section
    currentCategory = dlb() + '## ' + category.title()
    
    # Loop through every example in the category
    for sharedType in collection[category]:
        # Insert the shared type item in the index README
        headerReadmeContent += \
            lb() + ind() + \
            '- ' + sharedType
        
        for examplePath in collection[category][sharedType]:
            # Here we have to read the example yaml
            with open(examplePath, 'r') as stream:
                yml = yaml.safe_load(stream)

                if 'name' not in yml:
                    continue
                
                # Convert current type from plural to singular
                currentType = sharedType[:-1]
                
                # Insert the example list item in the index README
                nameUriEncoded = yml['name'].replace(' ', '-').lower()
                headerReadmeContent += \
                    lb() + ind() + ind() + \
                    '- [' + yml['name'] + '](#' + nameUriEncoded + ')'
                
                # Example title
                currentCategory += dlb() + '### ' + yml['name']
                
                # Example type
                grammar = 'a' if currentType == 'workflow' else 'an'
                currentCategory += dlb() + '_This is ' + grammar + ' ' + currentType + '_'

                # Example description
                if 'description' in yml:
                    currentCategory += dlb() + yml['description']
                    del yml['description']

                # Example author
                if 'author' in yml:
                    currentCategory += dlb() + '[Marketplace](' + yml['author'] + ')'
                    del yml['author']
                
                # Example code
                currentCategory += dlb() + 'How to invoke this ' + currentType + ':'
                
                import re
                fc = open(examplePath, 'r')
                # Remove description from example
                content = re.sub(r'^description.*\n?', '', fc.read(), flags=re.MULTILINE)
                # Remove author from example
                content = re.sub(r'^author.*\n?', '', content, flags=re.MULTILINE)
                fc.close()

                currentCategory += dlb() + \
                    '```yaml' + \
                    lb() + \
                    content + \
                    lb() + \
                    '```'
    
    # Write it to body README
    bodyReadmeConetent.append(currentCategory)

# Write it all to README
rootReadme = open('README.md', 'w')
rootReadme.write(headerReadmeContent + ''.join(bodyReadmeConetent))
rootReadme.close()
