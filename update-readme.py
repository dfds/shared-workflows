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

repoUri = 'https://github.com/dfds/shared-workflows/blob/master/workflows/'
examplesDir = 'examples'
rootReadmeContent = rootReadmeHeader()
 
for category in os.listdir(examplesDir):
    categoryPath = os.path.join(examplesDir, category)

    # Ignore files here
    if os.path.isfile(categoryPath):
        continue
    
    # Insert the category list item in the index README
    rootReadmeContent += lb() + '- [' + category.title() + '](' + repoUri + category + ')'

    # Initialize the category section
    currentCategory = '# ' + category.title()

    # Loop through every example in the category
    for example in os.listdir(categoryPath):
        examplePath = os.path.join(categoryPath, example)

        # Ignore folders here
        if os.path.isdir(examplePath):
            continue

        # Here we have to read the example yaml
        with open(examplePath, 'r') as stream:
            yml = yaml.safe_load(stream)

            if 'name' not in yml:
                continue
            
            # Insert the example list item in the index README
            nameUriEncoded = yml['name'].replace(' ', '-').lower()
            rootReadmeContent += \
                lb() + ind() + \
                '- [' + yml['name'] + '](' + repoUri + category + '#' + nameUriEncoded + ')'
            
            # Example title
            currentCategory += dlb() + '## ' + yml['name']

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
    
    # Write it all to category README
    categoryUriEncoded = category.replace(' ', '-').lower()
    rootReadme = open('workflows/' + category + '/README.md', 'w')
    rootReadme.write(currentCategory)
    rootReadme.close()

# Write it all to README
rootReadme = open('README.md', 'w')
rootReadme.write(rootReadmeContent)
rootReadme.close()
