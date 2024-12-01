from version import Version
from utils import optimizedSearch, getMatch

class OSDetector:
    """操作系统检测类"""
    def __init__(self):
        self.os = {
            'name': '',
            'version': None
        }

        # Windows 版本映射
        self._windows_versions = {
            '10.0.2': '11',
            '10.0': '10',
            '6.3': '8.1',
            '6.2': '8',
            '6.1': '7',
            '6.0': 'Vista',
            '5.2': 'Server 2003/XP x64',
            '5.1': 'XP',
            '5.0': '2000',
            '4.9': 'ME',
            '4.1': '98',
            '4.0': '95'
        }

    def detect(self, ua):
        """检测操作系统类型和版本"""
        # Harmony
        if optimizedSearch(r'OpenHarmony', ua):
            self.os['name'] = 'Harmony'
            match = optimizedSearch(r'OpenHarmony\s?([0-9.]+)', ua)
            if match:
                self.os['version'] = Version({'value': match.group(1)})
            return True

        # iOS
        elif optimizedSearch(r'iPhone|iPad|iPod', ua):
            self.os['name'] = 'iOS'
            match = optimizedSearch(r'OS ([\d_]+) like Mac OS X', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1).replace('_', '.')
                })
            return True

        # Android
        elif 'Android' in ua:
            self.os['name'] = 'Android'
            match = optimizedSearch(r'Android[\s\/]+([\d\.]+)', ua)
            if match:
                self.os['version'] = Version({'value': match.group(1)})
            return True

        # Windows
        elif 'Windows' in ua:
            self.os['name'] = 'Windows'
            # Windows NT 版本
            match = optimizedSearch(r'Windows NT ([\d\.]+)', ua)
            if match:
                nt_version = match.group(1)
                if nt_version in self._windows_versions:
                    version = self._windows_versions[nt_version]
                    self.os['version'] = Version({
                        'value': version,
                        'alias': version
                    })
            # Windows Phone
            elif 'Windows Phone' in ua:
                match = optimizedSearch(r'Windows Phone (?:OS )?([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
            return True

        # Mac OS X
        elif 'Mac OS X' in ua:
            self.os['name'] = 'Mac OS X'
            match = optimizedSearch(r'Mac OS X ([\d_\.]+)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1).replace('_', '.')
                })
            return True

        # Linux 发行版
        elif 'Linux' in ua:
            # Ubuntu
            if 'Ubuntu' in ua:
                self.os['name'] = 'Ubuntu'
                match = optimizedSearch(r'Ubuntu[\/\s]([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
                return True

            # CentOS
            elif 'CentOS' in ua:
                self.os['name'] = 'CentOS'
                match = optimizedSearch(r'CentOS[\/\s]+([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
                return True

            # Debian
            elif 'Debian' in ua:
                self.os['name'] = 'Debian'
                match = optimizedSearch(r'Debian[\/\s]+([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
                return True

            # Red Hat
            elif 'Red Hat' in ua:
                self.os['name'] = 'Red Hat'
                match = optimizedSearch(r'Red Hat[\/\s]+([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
                return True

            # Fedora
            elif 'Fedora' in ua:
                self.os['name'] = 'Fedora'
                match = optimizedSearch(r'Fedora[\/\s]+([\d\.]+)', ua)
                if match:
                    self.os['version'] = Version({'value': match.group(1)})
                return True

            # 通用 Linux
            self.os['name'] = 'Linux'
            return True

        return False