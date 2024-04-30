import concurrent.futures

from db.database import query_vods, process_data


def main():
    page = 0
    while True:
        page += 1
        records = query_vods(page, page_size=10)
        if not records:
            break

        # 使用线程池处理数据
        # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # 提交任务到线程池
        # futures = [executor.submit(process_data, record) for record in records]
        for record in records:
            process_data(record)

        # 等待所有线程完成
        # concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
