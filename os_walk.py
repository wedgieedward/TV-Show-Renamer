import os

for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print "subdirname"
        print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        print "filename"
        print os.path.join(dirname, filename)

    print "\n\n\n\n"
