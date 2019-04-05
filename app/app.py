import os
import random
import string
import sys
import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(format="%(message)s", level=logging.INFO)


class Config:

    def __init__(self,
                 pod_name,
                 delay_seconds,
                 use_log_message,
                 ):
        self.pod_name = pod_name
        self.delay_seconds = delay_seconds
        self.use_long_message = use_log_message

    def should_use_long_message(self):
        return self.use_long_message == 'yes'

    @staticmethod
    def from_env():
        pod_name = os.environ.get('HOSTNAME', 'undefined-host')
        delay_seconds = float(os.environ.get('DELAY_SECONDS', '0'))
        use_long_message = str(os.environ.get('USE_LONG_MESSAGE', 'yes'))
        config = Config(
            pod_name,
            delay_seconds,
            use_long_message,
        )
        return config


class App:

    def __init__(self):
        self.config = Config.from_env()
        self.msg_number = 0
        self.prev_msg_number = 0

    def run(self):
        payload = self.__random_payload()
        delay_seconds = self.config.delay_seconds
        self.start_stats_scheduler()
        while True:
            msg = "{} {}".format(self.msg_number, payload) if self.config.should_use_long_message() else self.msg_number
            logging.info(msg)
            if delay_seconds > 0:
                time.sleep(delay_seconds)
            self.msg_number += 1
            if self.msg_number == sys.maxsize:
                self.msg_number = 0

    def start_stats_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.log_stats, 'interval', minutes=1)
        # scheduler.add_job(self.log_stats, 'interval', seconds=1)
        scheduler.start()

    def log_stats(self):
        if self.msg_number < self.prev_msg_number:
            self.prev_msg_number = 0
        lpm = self.msg_number - self.prev_msg_number
        self.prev_msg_number = self.msg_number
        msg = f"appStats lpm: {lpm}, pod: {self.config.pod_name}"
        logging.info(msg)

    @staticmethod
    def __random_payload():
        characters = string.ascii_letters + string.digits
        # n = random.randrange(300, 500, 1)
        n = 500
        msg = ''.join(random.choice(characters) for x in range(n))
        return msg


if __name__ == '__main__':
    App().run()
