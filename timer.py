from datetime import datetime, timedelta


class Timer:
    def __init__(self, limit_time=30):
        # self.start_time = time.time()
        self.current_index = -1
        self.start_time = datetime.now()
        self.limit_time = self.start_time + timedelta(seconds=limit_time)

    def restart_timer(self):
        self.start_time = datetime.now()
        self.current_index = -1

    def check_timer(self):
        # current time - start_time < limit time
        # return self.current_index < self.limit_time
        return datetime.now() < self.limit_time

    def get_timer_counter(self):
        self.current_index += 1
        return self.current_index
