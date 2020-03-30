# My Portfolio
This is my portfolio.

## networking playground
jinja template tool
cisco configuration template
cisco autochecks

## route coverage checker
get FIB from router1
get FIB from router 2
allcovered = Yes
for each route in FIB.router1
    route is in FIB.router2
        noop
    else 
        print route
        allcovered = No
if allcovered
    print Yeah
else
    print Boo. Got some work to do.
