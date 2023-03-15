import requests

if __name__ == "__main__":
    r = requests.get(
        "http://127.0.0.1:8000/auto_api/auto-rides/vehicle/3000/",
        auth=("admin", "12345"),
        params={
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-02-01T00:00:00Z",
        },
    )
    print(f"Количество гео-точек -- {len(r.json())}")

    r = requests.get(
        "http://127.0.0.1:8000/auto_api/auto-rides/vehicle/3000/",
        auth=("admin", "12345"),
        params={
            "start_time": "2022-01-01T00:00:00Z",
            "end_time": "2022-02-01T00:00:00Z",
        },
    )
    print(f"Количество гео-точек -- {len(r.json())}")

    r = requests.get(
        "http://127.0.0.1:8000/auto_api/auto-rides/vehicle/3000/",
        auth=("admin", "12345"),
        params={
            "start_time": "2023-01-14T20:00:00Z",
            "end_time": "2023-02-01T00:00:00Z",
        },
    )
    print(f"Количество гео-точек -- {len(r.json())}")
