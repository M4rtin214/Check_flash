# Check_flash
- The script is for detection check of illuminated night photo. (traffic camera systems) 


**check_flash.py** - script for check illuminated of photo  
<pre>
output:  
True - the photo is illuminated 
False - the photo is not illuminated
None - out of the minimum count for check\another error
</pre>
         
         
**conf.ini** - configuration file

**check_flash_det.py** - script for setting values in the script configuration file "check_flash.py"
- Use the check_flash_det.py helper script to find and set the limit for determining the photo illumination in the conf.ini configuration file. Use a sample of illuminated and non-illuminated photos. 
