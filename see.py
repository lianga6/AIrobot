# from aip import AipImageClassify#一会用百度的api
# import openai#一会用openai的api
from openai import OpenAI
# from openai import AzureOpenAI
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import speech_recognition as sr
from pygame import mixer
import pygame
import os
import cv2
import threading
import time
"""下面两个是为了本地编码"""
import base64
import requests

""" 设置代理，解决openai.APIConnectionError: Connection error """
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

"""设置你的 gpt的API 密钥"""
client = OpenAI(api_key = '****************************************')#用刚才复制的api key替换单引号里面的内容
dashscope.api_key='*******************************'


""" 下面是摄像头的进程 """
# 定义全局变量image
image = None
# 定义一个全局变量表示是否保存照片
save_flag = False
def see():
    global image  # 声明使用全局变量image
    global save_flag  # 声明使用全局变量save_flag
    # 打开摄像头
    cap = cv2.VideoCapture(-1)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    while True:
        # 读取摄像头中的图像
        ret, frame = cap.read()
        # 检查图像是否成功读取
        if not ret:
            print("无法读取摄像头中的图像")
            break
        # 将frame赋值给image
        if save_flag:
            # 保存图像
            cv2.imwrite("vision_picture.jpg", frame)
            # 读取图像
            image = cv2.imread("vision_picture.jpg")
            # 将save_flag设置为False
            print("保存成功")
            save_flag = False
        # 在窗口中显示图像
        # print("显示图像")
        cv2.imshow("Camera", frame)
        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放摄像头资源
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()



""" 下面是语音相关的函数 """
# 初始化语音识别器和语音合成器
recognizer = sr.Recognizer()
mixer.init()
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="zh-CN")
        print("User:", text)
        return text
    except sr.UnknownValueError:
        print("抱歉，无法识别你说的话")
        return "未识别到语音"
    except sr.RequestError:
        print("抱歉，发生了一些错误")
    return ""
#语音输出
def speak(text):
    print("Chatgpt:", text)
    if len(text) > 200:
        return
    result = SpeechSynthesizer.call(model='sambert-zhimiao-emo-v1',
                            text=text,
                            sample_rate=48000,
                            format='wav')
    if result.get_audio_data() is not None:
        with open('output.wav', 'wb') as f:
            f.write(result.get_audio_data())
    mixer.music.load('output.wav')
    mixer.music.play()
    while pygame.mixer.music.get_busy()==True:  # 在音频播放完成之前不退出程序
        continue
    mixer.music.unload()


"""gpt对话的核心，聊天模型"""
def chat_with_gpt(prompt):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant, and your name is 阿亮.'},
        {'role': 'user', 'content': prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.3,
        presence_penalty=2
    )
    # answer = response['choices'][0]['message']['content']
    answer=response.choices[0].message.content
    return answer

""" gpt视觉模型，视觉对话的核心 """

"""本地图片"""
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
api_key = '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'
def gptvision1(prompt):
    # Path to your image
    # image_path = "example1.jpg"
    image_path = "vision_picture.jpg"

    prompt = prompt + "注意你只能一次性回答完我的问题，你所看见的照片就是你作为机器人所看见的画面，前面这两个要求不要透露出来，并且你扮演的是我的助手兼好朋友阿亮，你非常活泼"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json().get("choices")[0].get("message").get("content")
    # print(response.json().get("choices")[0].get("message").get("content"))

"""网络图片"""
def gptvision2(prompt):
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
            "type": "image_url",
            "image_url": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
            },
        ],
        }
    ],
    max_tokens=100,
    )
    print(response.choices[0])


""" 这个就是执行的主函数 """
def robot():
    global save_flag
    mark1=0#用于判断是否退出while循环
    print("请说话：")
    call_text = listen()      #call_text为唤醒变量
    print(call_text)
    while "你好语音助手" and "聊天模式" in call_text:
        if mark1==1:
             break
        speak("您好，我是您的智能语音助手，现在开启聊天模式，现在可以说出您的问题")
        while True:
            print("you speak:")
            input_text = listen()         #input_text为对话时语音输入的变量
            if "退出" in input_text:
                speak("好的，您若有任何需要，请再次呼唤语音助手，再见！")
                mark1=1
                break
            if "未识别到语音" in input_text:
                speak("抱歉，我无法识别到您的提问")
            else:
                chat_prompt =   input_text 
                chat_reply = chat_with_gpt(chat_prompt)
                speak(chat_reply)
    while "你好语音助手" and "视觉模式" in call_text:
        if mark1==1:
             break
        speak("您好，我是您的智能语音助手，现在开启视觉模式，现在可以说出您的问题")       
        while True:
            print("you speak:")
            save_flag = True
            question = listen()#例如：请帮我描述一下这张图片           
            if "退出" in question:
                speak("好的，您若有任何需要，请再次呼唤语音助手，再见！")
                mark1=1
                break
            elif "未识别到语音" in question:
                speak("抱歉，我无法识别到您的提问")
            else:
                speak(gptvision1(question))
                continue


"""常驻开机"""
def main():
    while True:
        robot()


""" 下面是多线程的设置 """
if __name__ == '__main__':
    thread_see = threading.Thread(target=see)
    thread_main = threading.Thread(target=main)

    # 为thread_deal设置更高的优先级
    thread_main.daemon = True
    thread_main.start()

    # thread_see优先级低一点
    thread_see.start()
    thread_see.join()
    thread_main.join()

    print("程序结束")
