"""
@Project   : text-classification-cnn-rnn
@Module    : multithreads.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/4/18 1:01 PM
@Desc      : 
"""
import os
import threading
from queue import Queue


# server.py，从网络有读入的消息，涉及I/O，同时对消息的及时的响应有要求，需要多线程，
# 每个线程都分到一定的执行时间，当用户数多于电脑核数的时候，光有多进程是不够的，每个核上
# 都要跑多线程

def start(self):
    """
    处理用户消息进程，消费src指定的队列中的消息，处理过后的结果存入dst中
    """
    self.prepare_actions()
    print("Server (%d) started, waiting data..." % os.getpid())
    thread_list = list()
    for _ in range(5):
        thread_consume = threading.Thread(target=self._do_consume)
        thread_list.append(thread_consume)
        thread_consume.start()

    for t in thread_list:
        t.join()


# chatbot.py，本质上是pipeline，这里的消费函数另起了子线程，因为主线程和网络有交互，
# 当用户多的时候，存在大量时间用于网络传输，这时利用子线程做意图处理就很有必要，另外，
# 为了及时的响应，似乎不该只开一条子线程，应该开多条子线程

def consume_intent_task(src: Queue, fun: callable, des: Queue,
                        redis: RedisPublish, rlog: RedisLog) -> threading.Thread:
    """
    消费意图线程函数，从q指定的缓存中获取意图和意图参数，传入fun指定的处理函数中
    :param src: 意图缓存
    :param fun: 处理意图的函数
    :param des: 意图处理结果缓存
    :param stop: stop标志位，为true时，停止线程
    :return: 返回消费线程handle
    """
    def _consume(_q: Queue, _fun, _d: Queue):
        while True:
            # 当本函数在服务器上执行的时候，由于循环不退出，该线程一直在执行，
            # 不断发送信息数据到redis
            try:
                context, msg_data = _q.get()
                result = _fun(context, msg_data)
                # **--> 在这里将处理结果压入结果队列中 <-- **
                # _d.put(result)
                # 这里适合用于多线程信息交互，如果是给其他服务器用，在Queue中是没用的
                rlog.log(result)
                redis.send(result)
                # 当有输出结果时，保存template---进入闲聊时会返回None，此时不保存
                if result:
                    context.save()

            except Exception as e:
                print("error@logic.chatbot, line 172: ", str(e))

    thread = threading.Thread(target=_consume, args=(src, fun, des))
    thread.start()
    return thread
