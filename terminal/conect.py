import paramiko
import os

class comand:

    def __init__(self):
        self.port = 22
        self.username = 'test'
        self.password = '1'
        self.path = '/home/test/alex/screen.png'
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def reboot_TO(self, ip):
        self.s.connect(ip, username=self.username, password=self.password)
        _stdin, stdout, stderr = self.s.exec_command("echo 1 | sudo -S sudo reboot")
        print(stdout.read().decode())
        print(stderr.read().decode())
        self.s.close()

    def screen(self, ip):
        print(self.s.connect(ip, username=self.username, password=self.password))
        check_file = os.path.exists(self.path)  # True
        if check_file:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.path)
            os.remove(path)
        self.s.connect(ip, username=self.username, password=self.password)
        _stdin, stdout, stderr = self.s.exec_command('DISPLAY=:0 gnome-screenshot --file={}'.format(self.path))
        print(stdout.read().decode())
        print(stderr.read().decode())
        ftp_client = self.s.open_sftp()
        ftp_client.get(self.path, '{}.png'.format(ip))
        self.s.close()

    def reboot_mie(self, ip):
        self.s.connect(ip, username=self.username, password=self.password)
        _stdin, stdout, stderr = self.s.exec_command("echo 1 | sudo -S sudo python3.6 /home/test/alex/mie_003.py")
        print(stdout.read().decode())
        print(stderr.read().decode())
        self.s.close()

