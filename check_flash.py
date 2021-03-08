# input arguments: idCAM
# - values of variables in the file conf.ini
# output: 
#        True - the photo is illuminated 
#        False - the photo is not illuminated
#        None - out of the minimum count for check\other error
# version: Python 2.7


from datetime import datetime
from os import walk
import sys
import ConfigParser
from colorthief import ColorThief
from pyzabbix import ZabbixMetric, ZabbixSender

#zabbix host,item value: (load data of config file conf.ini)
Config_file = ConfigParser.ConfigParser()
Config_file.read('conf.ini')
zabbix_server = str(Config_file.get('ZabbixSenderParameter', 'zabbix_server')) #IP address Zabbix server
host = str(Config_file.get('ZabbixSenderParameter', 'host')) #hostname of zabbix
key = str(Config_file.get('ZabbixSenderParameter', 'key'))  #key item
rgb1_limit = int(Config_file.get('ZabbixSenderParameter', 'rgb1_limit')) #limit RGB1
rgb2_limit = int(Config_file.get('ZabbixSenderParameter', 'rgb2_limit')) #limit RGB2
rgb3_limit = int(Config_file.get('ZabbixSenderParameter', 'rgb3_limit')) #limit RGB3

value = ""

#detection value:
PHOTO_DETECTION = 8 #number of photos to detect
PHOTO_CONFRIM = 2 #number of photos to confirm detection

#argument:
idCAM = str(sys.argv[1])

# sent to Zabbix
def zabbix_send_to_trapper(zabbix_server,host, key,value):
    metrics = [ZabbixMetric(host, key, value)]
    result_sent = ZabbixSender(zabbix_server=zabbix_server, zabbix_port=10051).send(metrics)
    print ("ZabbixSender status: ", result_sent)
    return result_sent

# get actual file path 
def file_path():
    now = datetime.utcnow()  
    now = str(now)
    now = now[0:10]
    year = now[0:4]
    month = now[5:7]
    day = now[8:10]
    hour =datetime.utcnow().hour
    if int(hour) < 10:
        hour = "0" + str(hour)
    path = "D:\\RRC-M\\data\\images\\vehicle-sequence\\"
    file_path = path + str(year) +"\\" + str(month) + "\\" + str(day) + "\\" + str(hour) + "\\" + idCAM + "\\"  #dynamic file path 
    return file_path

# returns a list of file names
def files_of_folder(path):
    files_lst = []
    for (dirpath, dirnames, filenames) in walk(path):
        files_lst.extend(filenames)
        break
    return files_lst

#returns a list with information about the dominant color in RGB(x,x,x)
def dominant_color(img):
    color_thief = ColorThief(img)
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    img_rgb_lst = dominant_color
    return img_rgb_lst

if __name__ == "__main__":
    file_path = file_path()
    files_lst = files_of_folder(file_path)
    #print (file_path)
    #print (files_lst)
    if len(files_lst) < PHOTO_DETECTION:
        value = "None"
        send_result_to_zabbix = zabbix_send_to_trapper(zabbix_server, host, key, value)
        sys.exit(1)

    step = 0
    flash = 0
    try:
        for img in files_lst:
            step = step + 1
            if step > PHOTO_DETECTION:
                break
            img = str(file_path + img)
            result = dominant_color(img)
            rgb1 = result[0]
            rgb2 = result[1]
            rgb3 = result[2]

            if rgb1 > rgb1_limit and rgb2 > rgb2_limit and rgb3 > rgb3_limit:
                flash = flash + 1
            if flash >= PHOTO_CONFRIM:
                break
    except:
        value = "None"
        send_result_to_zabbix = zabbix_send_to_trapper(zabbix_server, host, key, value)
        sys.exit(1)

    if flash >= PHOTO_CONFRIM:
        value = "True"
        send_result_to_zabbix = zabbix_send_to_trapper(zabbix_server, host, key, value)
        sys.exit(0)
    else:
        value = "False"
        send_result_to_zabbix = zabbix_send_to_trapper(zabbix_server, host, key, value)
        sys.exit(0)


















