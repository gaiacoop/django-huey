queues = {
    "test": {
        "huey_class": "huey.MemoryHuey",
        "results": True,
        "store_none": False,
        "immediate": False,
        "utc": True,
        "blocking": True,
        "consumer": {
            "workers": 1,
            "worker_type": "thread",
            "initial_delay": 0.1,
            "backoff": 1.15,
            "max_delay": 10.0,
            "scheduler_interval": 60,
            "periodic": True,
            "check_worker_health": True,
            "health_check_interval": 300,
        },
    },
}
