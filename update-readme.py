#!/usr/bin/env python

import os
import yaml

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

repoUri = 'https://github.com/dfds/shared-workflows'
examplesDir = 'examples'
headerReadmeContent = rootReadmeHeader()
bodyReadmeConetent = []
collection = {}

# Create example collection
for example in os.listdir(examplesDir):
    examplePath = os.path.join(examplesDir, example)

    # Ignore folders here
    if os.path.isdir(examplePath):
        continue

    # Extract the category from filename
    category = example.split('-')[0]

    if not category in collection.keys():
        collection[category] = []
    
    collection[category].append(examplePath)

for category in collection:
    # Insert the category list item in the index README
    headerReadmeContent += lb() + '- [' + category.title() + '](' + repoUri + '#' + category + ')'

    # Initialize the category section
    currentCategory = dlb() + '## ' + category.title()
    
    # Loop through every example in the category
    for examplePath in collection[category]:
        # Here we have to read the example yaml
        with open(examplePath, 'r') as stream:
            yml = yaml.safe_load(stream)

            if 'name' not in yml:
                continue
            
            # Insert the example list item in the index README
            nameUriEncoded = yml['name'].replace(' ', '-').lower()
            headerReadmeContent += \
                lb() + ind() + \
                '- [' + yml['name'] + '](' + repoUri + '#' + nameUriEncoded + ')'
            
            # Example title
            currentCategory += dlb() + '### ' + yml['name']

            # Example description
            if 'description' in yml:
                currentCategory += dlb() + yml['description']
                del yml['description']

            # Example author
            if 'author' in yml:
                currentCategory += dlb() + '[Marketplace](' + yml['author'] + ')'
                del yml['author']
            
            # Example code
            currentCategory += dlb() + 'How to invoke this shared workflow:'
            
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
