#coding=utf-8

import logging

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                        filename='if_running.log',
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        # format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        format = '%(asctime)s  - %(levelname)s: %(message)s'
                        # 日志格式
                        )


def log(message):
    logging.info(message)
    print(message)


if __name__ == '__main__':
    log('test')
    print(str('test'))