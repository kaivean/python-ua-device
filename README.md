# ua-device 2.0
解析user-agent的python包，可以获取到系统、浏览器内核、浏览器、设备信息。

## 重要提示：2.0版本重大变更
⚠️ 2.0版本进行了完全重构，与1.x版本不兼容。主要变更：

1. **简化代码结构**
   - 删除了大量历史设备和过时浏览器的识别规则
   - 重构了核心解析逻辑，提升执行效率
   - 代码结构更清晰，便于维护和扩展

2. **功能优化**
   - 优化了浏览器内核识别逻辑，准确区分Blink和WebKit
   - 聚焦于主流设备和浏览器的识别
   - 移除了低使用率的特殊规则

3. **性能提升**
   - 减少正则表达式的使用
   - 优化了匹配算法
   - 显著提升解析速度

如果您需要继续使用旧版本的完整功能，请安装1.x版本：

```bash
pip install "uaDevice<2.0"
```

## 特点
* 相比国内外的流行的python包，该模块解析国内复杂的ua信息更加精确
* 已支持鸿蒙系统解析
* 准确识别Blink/WebKit等主流浏览器内核
* 专注于现代浏览器和设备的识别

## 主要功能

### 1. 浏览器引擎识别
* Blink (Chrome、新版Edge等)
* WebKit (Safari等)
* Gecko (Firefox)
* Trident (IE)
* Presto (旧版Opera)

### 2. 浏览器识别
* 主流浏览器：Chrome、Firefox、Safari、Edge等
* 国内浏览器：QQ浏览器、UC浏览器、搜狗浏览器等
* 手机厂商浏览器：MIUI浏览器、华为浏览器、OPPO浏览器等
* 其他常用浏览器：微信内置浏览器、百度App等

### 3. 系统识别
* 桌面系统：Windows、macOS、Linux等
* 移动系统：iOS、Android、Harmony等

### 4. 设备识别
* 设备类型：手机、平板、桌面设备等
* 设备品牌：Apple、Samsung、Huawei等
* 具体机型识别

## 解析成功率
供参考（以10000个真实请求ua测试）:
* 浏览器：98%
* 系统： 99%
* 内核： 98%
* 设备类型： 100%
* 设备型号：86%
* 厂商信息：93%

## 安装

```bash
pip install -U uaDevice
```

## 使用

```python
import uaDevice

# Chrome浏览器示例
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
info = uaDevice.parseUA(ua)

# 输出结果示例
print(f"系统: {info['os']['name']} {info['os']['version']['original']}")  # Windows 10.0
print(f"浏览器: {info['browser']['name']} {info['browser']['version']['original']}")  # Chrome 91.0.4472.124
print(f"内核: {info['engine']['name']} {info['engine']['version']['original']}")  # Blink 537.36
print(f"设备类型: {info['device']['type']}")  # desktop
print(f"设备型号: {info['device']['model']}")  # PC
print(f"制造商: {info['device']['manufacturer']}")  # Unknown

# 微信内置浏览器示例
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000731) NetType/WIFI Language/zh_CN'
info = uaDevice.parseUA(ua)
# 将识别出微信浏览器、iOS系统、iPhone设备等信息
```

## 特性说明

1. **智能内核识别**
   - 准确区分Blink和WebKit内核
   - 支持版本号解析
   - 处理特殊情况（如IE的Trident版本映射）

2. **设备识别优化**
   - 通过机型识别品牌
   - 处理国内厂商特殊UA格式
   - 机型别名统一处理

3. **浏览器识别优化**
   - 支持国内主流浏览器
   - 处理WebView场景
   - 区分股票和定制浏览器

## 贡献
随着新设备新app等等的上市，ua信息会越来越复杂，该项目需要不断迭代，欢迎提交PR或Issue来完善不支持的ua解析规则。

## 感谢
该项目基于fex团队维护的js版本ua解析库[ua-device](https://github.com/fex-team/ua-device)重构优化。