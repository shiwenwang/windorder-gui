from ftplib import FTP, error_perm
import socket
import re


class MyFTP:
    def __init__(self, host, port=21, user='', passwd=''):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def connect(self):
        try:
            with FTP(self.host) as ftp:
                ftp.login()
        except (error_perm, socket.gaierror, TimeoutError) as e:
            return False, e

        return True

    def check_update(self, current_version):
        pattern = re.compile(r'([0-9]+\.[0-9]+)')
        current_version_no = float(pattern.search(current_version).group(0))
        connect = self.connect()
        if connect[0]:
            with FTP(self.host) as ftp:
                ftp.login()
                ftp.cwd('/')
                dir_list = ftp.nlst()
                latest_version_no = float(pattern.search(dir_list[-1]).group(0))
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
    ftp = MyFTP('10.11.52.185')
    result = ftp.check_update('1.1')
    if result[0]:
        ftp.download('D://1.zip', os.path.join('/', result[1], result[1]+'.zip'))
    pass