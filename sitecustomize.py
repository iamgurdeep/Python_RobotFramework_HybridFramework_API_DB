import site
import os



# Setting up Project Base Dir change your base dir here - Gurdeep
import sys

curdir = 'D:\\Catalog'
# curdir = os.getcwd()
print(f"Framework's Base Location being used is {curdir}")
print ('Catalog Management TestCase Execution Starting.Please Wait....')


# Adding new Customized Site Packages
site.addsitedir(curdir)
site.addsitedir(curdir+'\\Data')
site.addsitedir(curdir+'\\libraries')
site.addsitedir(curdir+'\\libraries\\main')
site.addsitedir(curdir+'\\libraries\\Tax')
site.addsitedir(curdir+'\\libraries\\Catalog')

# print(sys.path)

