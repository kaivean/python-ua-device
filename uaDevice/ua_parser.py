from version import Version
from browser_detector import BrowserDetector
from os_detector import OSDetector
from device_detector import DeviceDetector

class UAParser:
    """UA 解析主类"""
    def __init__(self, ua='', options=None):
        self.options = options or {}

        # 初始化检测器
        self.browser_detector = BrowserDetector()
        self.os_detector = OSDetector()
        self.device_detector = DeviceDetector()

        # 如果提供了 UA，立即解析
        if ua:
            self.parse(ua)

    def parse(self, ua):
        """解析 UA 字符串"""
        if not ua:
            return self

        # 按顺序进行检测
        self.browser_detector.detect(ua)
        self.os_detector.detect(ua)
        self.device_detector.detect(ua)

        return self

    def get_result(self):
        """获取解析结果"""
        return {
            'browser': {
                'name': self.browser_detector.browser['name'],
                'version': {
                    'original': str(self.browser_detector.browser['version']) if self.browser_detector.browser['version'] else '',
                    'alias': self.browser_detector.browser['version'].alias if self.browser_detector.browser['version'] else ''
                },
                'mode': self.browser_detector.browser['mode'],
                'channel': self.browser_detector.browser['channel']
            },
            'engine': {
                'name': self.browser_detector.engine['name'],
                'version': {
                    'original': str(self.browser_detector.engine['version']) if self.browser_detector.engine['version'] else '',
                    'alias': self.browser_detector.engine['version'].alias if self.browser_detector.engine['version'] else ''
                }
            },
            'os': {
                'name': self.os_detector.os['name'],
                'version': {
                    'original': str(self.os_detector.os['version']) if self.os_detector.os['version'] else '',
                    'alias': self.os_detector.os['version'].alias if self.os_detector.os['version'] else ''
                }
            },
            'device': {
                'type': self.device_detector.device['type'],
                'manufacturer': self.device_detector.device['manufacturer'],
                'model': self.device_detector.device['model']
            }
        }

def parseUA(ua, options=None):
    """便捷解析函数"""
    parser = UAParser(ua, options)
    return parser.get_result()

def format_result(result):
    """格式化结果为字符串"""
    device_info = []
    if result['device']['manufacturer']:
        device_info.append(result['device']['manufacturer'])
    if result['device']['model']:
        device_info.append(result['device']['model'])

    os_info = result['os']['name']
    if result['os']['version']['original']:
        os_info += ' ' + result['os']['version']['original']

    browser_info = result['browser']['name']
    if result['browser']['version']['original']:
        browser_info += ' ' + result['browser']['version']['original']

    parts = []
    if device_info:
        parts.append(' '.join(device_info))
    if os_info:
        parts.append(os_info)
    if browser_info:
        parts.append(browser_info)

    return ' / '.join(parts)

# 示例用法
if __name__ == '__main__':
    test_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
    result = parseUA(test_ua)
    print(format_result(result))
    # 输出示例: Apple iPhone / iOS 14.4 / Safari 14.0.3