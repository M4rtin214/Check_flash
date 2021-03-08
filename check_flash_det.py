# input argument: file path ex.:"x:\\MUR\\Stanoviste_TMP\\all\\21-01-21\\02hod\\cam1"

from colorthief import ColorThief
from os import walk
import sys


#argument:
try:
    file_path = str(sys.argv[1])
    if file_path[-1:] != "\\":
        file_path = file_path + "\\"
except:
    print ("Invalid argument file path!")
    sys.exit(1)

# returns a list of file names
def files_of_folder(path):
    files_lst = []
    for (dirpath, dirnames, filenames) in walk(path):
        files_lst.extend(filenames)
        break
    return files_lst

# returns a list with information about the dominant color in RGB(x,x,x)
def dominant_color(img):
    color_thief = ColorThief(img)
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    img_rgb_lst = dominant_color
    return img_rgb_lst

if __name__ == "__main__":
    files_lst = files_of_folder(file_path)
    print ("path: ", file_path)
    #print ("files: ", files_lst)
    step = 0
    flash = 0

    for img in files_lst:
        step = step + 1

        print ("step:", step)
        img = str(file_path + img)
        print (img)
        result = dominant_color(img)
        print (result)   
    sys.exit(0)


















