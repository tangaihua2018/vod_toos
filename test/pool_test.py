import concurrent.futures
from time import sleep


def main():
    ls = [l for l in range(0, 1000)]

    # 使用线程池处理数据
    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
        # 提交任务到线程池
        futures = [executor.submit(print_delay, record) for record in ls]

        # 等待所有线程完成
        concurrent.futures.wait(futures)

def print_r(info):
    print(i)
    sleep(1)

if __name__ == '__main__':
    main()
