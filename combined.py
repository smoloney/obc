import os
import urllib
import requests
import shutil
from pathlib import Path
from PIL import Image
from glob import glob

path = "OBCImages"
Image.MAX_IMAGE_PIXELS = None

sizes = {
    "6x22": (5.75, 21.75),
    #"8x11":(9.25,12.25),
    "9x12": (9, 12),
    "10x24": (10.625, 24),
    "12x16":(12, 16.13),
    "13x13": (13, 13),
    "14x20": (14, 20),
    "14x32": (14, 32),
    "18x18":(18, 18),
    "18x24":(17.75, 24),
    "25x34":(24.75, 33),
    "30x30":(30,30),
    "30x40":(30, 40)
}




def createandNav():


    urlfile = raw_input("Enter file name for URLs: ")
    ordernumberfile = raw_input("Enter file name for order numbers: ")
    with open(urlfile, "r") as ins:
        array = []
        for line in ins:
            array.append(line)

    numArray = open(ordernumberfile).read().split('\n')
    img = urllib.URLopener()
    print ("Making OBC Images Directory")
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)
    os.getcwd()

    
    for i in range (len(array)):
        print "Downloading image..."
        s = str(numArray[i])
        if(s[len(s)-4] == '?'):
            
            filename = s[:len(s)-1] + ".jpg"
        else:
            filename = s + ".jpg"
        url = array[i]


        if(url[12:19] == 'dropbox' or url[7:15] == 'uploadery'):
            downloadFiles(url, filename, path)
        else:
            if (url[4] == 's'):
                url = url[:4]+url[5:]
            filename = str(numArray[i]) + ".jpg"
           
            try:
                img.retrieve(url, filename)
            except:
                print('Error in url:'+ url)
                exit()

        searchForDir(filename)
    print ("Complete! Exiting.")
    exit() 

def searchForDir(img):
    resize = Image.open(img)
    dictDir = str(resize.size[0]/300)+"x"+str(resize.size[1]/300) # Duplicate
    attempts = 4
    resizeWidth = 0
    resizeHeight = 0
    doesExist = Path(os.getcwd()+"/"+dictDir+"/"+img)

    if doesExist.is_file():
        print("File already exists...\nSkipping...")
        os.remove(os.getcwd()+"/"+img)
        return
    
    for i in range(1, attempts):
        if(resize.info['dpi'][0] != 300 or resize.info['dpi'][1] != 300):
          incorrectImage(img)
          return
        try:
            (resizeWidth, resizeHeight) = sizes[dictDir]            # This loop is likely the issue with
        except KeyError:                                            # the sizing issue.  Creating image of wrong dpi
            incorrectImage(img)
            return

        break

    dirName = str(int(resize.size[0]/300))+ "x"+str(int(resize.size[1]/300)) # Duplicate 
    if not os.path.exists(os.getcwd()+"/" + dirName):
        print("Found a new size.  Making a directory")
        os.makedirs(os.getcwd()+"/" + dirName)
    print("Resizing image...")
    resizeImage(img, resizeWidth, resizeHeight)
    print("Moving it to the correct folder...\n\n")
    shutil.move(os.getcwd()+ "/" + img, os.getcwd()+"/"+ dirName + "/" + img)

def incorrectImage(img):
    print("\nError! The image " + str(glob("*.jpg"))+ " is the incorrect size or dpi.  Please check the original image.")
    print("After the image is fixed, rerun this script.")

    if not os.path.exists(os.getcwd()+"/fix/"):
        os.makedirs(os.getcwd()+"/fix/")

    shutil.move(os.getcwd()+ "/" + img, os.getcwd()+ "/fix/"+ img)

def resizeImage(img, width, height):

    resizeWidth = int(width) * 300
    resizeHeight = int(height) * 300
    newImage = Image.open(img)
    newImage = newImage.resize((resizeWidth, resizeHeight), Image.BILINEAR)
    newImage.save(img, format='JPEG', dpi=newImage.info['dpi'])



def downloadFiles(url, filename, path):
    try:
        downloaded_file = requests.get(url)
    except:
        print("Error in url: %s", (url))
        exit()
    destFile = open(os.getcwd()+'/'+filename, 'w+')
    destFile.write(downloaded_file.content)
   




createandNav()
