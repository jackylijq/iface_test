#coding=utf-8
import random,os,string
from threading import Thread
path = 'f:/test/'


class create_file():
    #随机生成一串字符串，包含特殊字符
    def ranstr(self,num):
        # 猜猜变量名为啥叫 H
        special_character= '$_'
        target_str = ''.join(random.sample(string.ascii_letters + string.digits, num))
        target_str = target_str + random.choice(special_character)
        # print(target_str)
        return target_str

    def genSizeFile(self,fileSize):
        # file path
        fileName = self.ranstr(32) + str(random.randint(99,999999))
        filePath = path + "data_" + fileName + ".txt"

        # 生成固定大小的文件
        # date size
        ds = 0
        #设置默认一行字符数，根据当前字符数量进行数据计算
        row_size = 1024*1024 if fileSize > fileSize else fileSize
        while ds < fileSize:
            file = open(filePath, 'a+', encoding='utf-8')
            target_str = ''
            for i in range(100):
                target_str = target_str + target_str + self.ranstr(32)
                if len(target_str) >= row_size:
                    break
            file.write(target_str)
            file.write("\n")
            file.close()
            ds = os.path.getsize(filePath)
            if ds % 1024 == 0:
                print(u'当前文件名称：%s,当前文件大小：%s kb' %(filePath,str(ds/1024)))


    def createfile(self,number,size):
        for i in range(number):
            self.genSizeFile('a'+str(i),size*1024*1024)

    #多线程并发
    def thread_batch(self,number,size):
        l_thread = (Thread(target=self.genSizeFile, args=(size*1024*1024,)) for i in range(number))
        for t in l_thread:
            t.start()  # 启动线程开始执行


if __name__ == '__main__':
    create_file_instances = create_file()
    #文件存储的绝对路径：路径需要手动创建
    path = '/home/test/test1234/'
    #第一个参数为需要生成的文件格式，第二个参数为当前文件的大小，单位M
    create_file_instances.thread_batch(100000,0.1)