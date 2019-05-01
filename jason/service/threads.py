import threading


class AppThreads:
    def __init__(self):
        self.app = None
        self.config = None
        self._app_threads = []

    def init_app(self, app, config):
        self.app = app
        self.config = config
        self.app.before_first_request(self.run_all)
        self.app.extensions["app_threads"] = self

    def add(self, method, args=None, kwargs=None):
        self._app_threads.append(
            {"method": method, "args": args or (), "kwargs": kwargs or {}}
        )

    def run_all(self):
        for process in self._app_threads:
            thread = threading.Thread(
                target=process["method"], args=process["args"], kwargs=process["kwargs"]
            )
            thread.start()
