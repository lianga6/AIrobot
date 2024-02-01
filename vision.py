
from aip import AipImageClassify
import os
print("当前工作目录:", os.getcwd())


""" 你的 APPID AK SK """
APP_ID = '***************'
API_KEY = '*****************'
SECRET_KEY = '******************'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('example.jpg')

""" 调用菜品识别 """
client.dishDetect(image)

""" 如果有可选参数 """
options = {}
options["top_num"] = 3
options["filter_threshold"] = "0.7"
options["baike_num"] = 5

""" 带参数调用菜品识别 """
print(client.dishDetect(image, options))
