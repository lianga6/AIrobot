# AIrobot
本项目我将其命名为AIrobot，其实就是个智能语音系统，它有两种模式，其一是聊天模式，需要用“你好语音助手，请开启聊天模式”来使其响应，用的是ChatGPT的gpt3.5的模型，聊天模式是有记忆的；其二是视觉模式，需要用“你好语音助手，请开启视觉模式”来使其响应，用的是gpt4-version模型，可以通过视觉与外界交互。

本项目可在你的PC上运行，Windows系统和Linux系统都可以，也可以在树莓派这样的嵌入式系统上运行。
如果你需要在树莓派这样的嵌入式系统上运行，那么你需要自己准备麦克风，扬声器和摄像头（最好都准备免驱的）
主要使用的代码文件时see.py,see1.py更完善，后续会进行see2.py的编写，see2.py的前身是vision.py, see2.py会加入专业的某些场景识别，比如菜品识别，车辆识别，logo识别等等
代码中你需要改的是：
client = OpenAI(api_key = '***********************)和
dashscope.api_key='***********************'
这两个api的获取参考：
https://zhuanlan.zhihu.com/p/640573773
https://help.aliyun.com/zh/dashscope/developer-reference/api-key-settings


下面是遇到的问题及解决办法
1.首先是alsa的问题，比如说找不到声卡啊什么的，因为alsa默认设置时声卡0，而此项目麦克风使用的是声卡3，可通过aplay -l显示出来，扬声器使用的是声卡2，可通过arecord -l来显示出来。自定义配置的话是修改配置文件~/.asoundrc或者文件/etc/asound.conf
  判断是哪个声卡录音可以使用arecord -D hw:3,0 -r 44100 -f S16_LE test2.wav命令来进行测试，其中那个3是声卡的ID，可用arecord -l来看，0是device（一般都是0）
  判断是哪个声卡播音可以使用aplay -D hw:0,0 test.wav命令来进行测试
  可参考文献 https://blog.csdn.net/weixin_41965270/article/details/81272710
            https://blog.csdn.net/lile777/article/details/62428473
            https://wiki.archlinuxcn.org/wiki/ALSA/%E7%96%91%E9%9A%BE%E8%A7%A3%E7%AD%94#%E9%BA%A6%E5%85%8B%E9%A3%8E
            https://www.alsa-project.org/main/index.php/Asoundrc
            https://www.cnblogs.com/spjy/p/7085281.html
2.其次是摄像头的问题，我的树莓派的默认摄像头接口坏了，所以买了一个免驱的USB摄像头，一般来说默认的摄像头ID就是0，即cap = cv2.VideoCapture(0)，但有时候也不一定，所以可能需要你用cameraID.py来测试出摄像头的ID。
3.最后是whisper下载的问题，一定要注意下载的是openai的whisper，不然会吃大亏。
4.既然使用了openai的API，你懂的


视频：https://github.com/lianga6/AIrobot/assets/117170749/9da16bfc-1469-4460-82c3-ac1e33b3063d


