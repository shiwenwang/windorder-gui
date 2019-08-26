from ftplib import FTP, error_perm
import socket
import re
import os
import subprocess

class MyFTP:
    def __init__(self, host, port=21, user='', passwd=''):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def connect(self):
        test_result = self.ip_ping_test()
        if test_result:
            return False, TimeoutError
        else:
            try:
                with FTP(self.host) as ftp:
                    ftp.login()
            except (error_perm, socket.gaierror, TimeoutError) as e:
                return False, e

            return True, 

    def ip_ping_test(self):
        ret = subprocess.Popen(f"ping -n 1 -w 1 {self.host}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = [i.decode("gbk") for i in ret.communicate()]
        pattern = re.compile(r'丢失 = (\d) ')
        m = pattern.search(ret[0])
        
        return int(m.groups()[0])

    def check_update(self, current_version):
        pattern = re.compile(r'.*?(\d*)\.*(\d*)\.*(\d*).*?')
        m = pattern.search(current_version)
        current_version_no = int(''.join([m.groups()[0], m.groups()[1], m.groups()[2]]))
        connect = self.connect()
        if connect[0]:
            with FTP(self.host) as ftp:
                ftp.login()
                ftp.cwd('/')
                dir_list = ftp.nlst()
                pattern = re.compile(r'WindOrder-v(\d*)\.*(\d*)\.*(\d*).*')
                m = pattern.search(dir_list[-1])
                latest_version_no = int(''.join([m.groups()[0], m.groups()[1], m.groups()[2]]))
                new_release_name = dir_list[-1]
                if latest_version_no > current_version_no:
                    return True, new_release_name
                else:
                    return False, '暂无更新'
        else:
            if isinstance(connect[1], TimeoutError):
                return False, '主机长时间没有响应，连接尝试失败'
            else:
                return False, '连接错误，检查失败'

    def download(self, local_file, remote_file):
        with FTP(self.host) as ftp:
            ftp.login()
            ftp.cwd('/')
            file_handler = open(local_file, 'wb')
            ftp.retrbinary('RETR ' + remote_file, file_handler.write)
            file_handler.close()

        return True


if __name__ == "__main__":
    import os
    ftp = MyFTP('192.168.199.249')
    result = ftp.check_update('1.0')
    if result[0]:
        ftp.download('D://1.7z', os.path.join('/', result[1], result[1]+'.7z'))
    else:
        print('连接失败')

    # import subprocess
    # import re
    # ret = subprocess.Popen(f"ping -n 1 -w 1 10.11.52.185", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # # out = p.stdout.read()
    # print([i.decode("gbk") for i in ret.communicate()])
    # # regex = re.compile("Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", re.IGNORECASE)
    # # print(regex.findall(out))
    # # 192.168.199.249