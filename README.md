# Check_flash
The script is for detection check of illuminated night photo. (traffic camera systems) 


check_flash.py - Script for check illuminated of photo
  output: 
         True - the photo is illuminated 
         False - the photo is not illuminated
         None - out of the minimum count for check\another error
         
conf.ini - configuration file

check_flash_det.py - Script for setting values in the script configuration file "check_flash.py"
- Using the helper script check_flash_det.py, find and set the limit for photo illumination in the configuration file conf.ini.
