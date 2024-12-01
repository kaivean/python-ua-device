class Version:
    """版本信息类"""
    def __init__(self, v=None):
        """
        初始化版本信息
        v: 字典类型，包含 value(原始版本号)、alias(别名)、details(详细信息) 等字段
        """
        v = v or {}
        self.original = v.get('value', '')  # 原始版本号
        self.alias = v.get('alias', '')     # 版本别名
        self.details = v.get('details', None)  # 详细信息
        self.minor = -1    # 次版本号
        self.type = ''     # 版本类型

    def __str__(self):
        """字符串表示"""
        return self.original

    def is_equal(self, v):
        """判断版本是否相等"""
        if not v:
            return False
        return self.original == v

    def is_greater_than(self, v):
        """判断是否大于指定版本"""
        if not v:
            return False
        try:
            current = [int(x) for x in self.original.split('.')]
            compare = [int(x) for x in str(v).split('.')]
            return current > compare
        except (ValueError, AttributeError):
            return False

    def is_less_than(self, v):
        """判断是否小于指定版本"""
        if not v:
            return False
        try:
            current = [int(x) for x in self.original.split('.')]
            compare = [int(x) for x in str(v).split('.')]
            return current < compare
        except (ValueError, AttributeError):
            return False