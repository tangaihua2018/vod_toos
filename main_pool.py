from db.database import query_vods, process_data


def main():
    page = 0
    while True:
        page += 1
        records = query_vods(page, page_size=20)
        if not records:
            break

        for record in records:
            process_data(record)


if __name__ == "__main__":
    main()
