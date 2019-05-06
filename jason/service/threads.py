import threading


class ServiceThreads:
    def __init__(self):
        self.app = None
        self._service_threads = []

    def init_app(self, app):
        self.app = app
        self.app.before_first_request(self.run_all)
        self.app.extensions["service_threads"] = self

    def add(self, method):
        self._service_threads.append({"method": method, "kwargs": {"app": self.app}})

    def run_all(self):
        for process in self._service_threads:
            thread = threading.Thread(
                target=process["method"], kwargs=process["kwargs"]
            )
            thread.start()

    def thread(self, func):
        self.add(method=func)
        return func
