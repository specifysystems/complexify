"""Module containing the job flow daemon process."""
import time

class JobFlowDaemon:
    def __init__(self):
        pass
    def run(self):
        while True:
            print('Still running, sleep 60 seconds')
            time.sleep(60)
    def start(self):
        self.run()

if __name__ == '__main__':
    jf_daemon = JobFlowDaemon()
    jf_daemon.start()
