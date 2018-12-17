# ua-device [![Build Status](https://travis-ci.com/kaivean/python-ua-device.svg?branch=master)](https://travis-ci.com/kaivean/python-ua-device)
解析user-agent的python包，可以获取到系统、浏览器内核、浏览器、设备信息，其特点：

* 相比国内外的流行的python包，该模块解析国内复杂的ua信息更加精确，有几千行代码专门来匹配具体的特定的ua

## Why

由于在国内生产PC的厂家有限，大众用户使用的浏览器也主要是当前的一些主流浏览器。因此目前的UA解析库在对OS、浏览器外壳、浏览器内核等的识别率都相当高。但是由于国内的移动设备的五花八门，对于移动设备的硬件信息是很难用一套通用的方法进行识别，因此 ua-device 诞生

* 通过机型识别品牌: 例如 [-\s](Galaxy[\s-_]nexus|Galaxy[\s-_]\w*[\s-_]\w*|Galaxy[\s-_]\w*|SM-\w*|GT-\w*|s[cgp]h-\w*|shw-\w* 这样的匹配规则以及一些从中关村在线爬取到的机型名称如G3508、G3508J、G3508i 等识别出来该机型的品牌为Samsung 因为单纯从UA信息确实无法得到品牌数据，这也是为何很多高Star的UA解析库识别手机品牌成功率只有30%-40%的原因(ua-device识别率可见下面测试用例)。
* 解决国内UA信息不规范: 由于国内很多手机生产厂家的设计问题，例如小米可供识别的UA数据可能为 mi 2 、mi2、m2、mi-2LTE、MI-20150XX、minote等等，如果匹配规则限制太紧就会导致数据无法命中，如果匹配规则太松又会让其它山寨机型滥竽充数，所以需要一套比较特殊的处理流程。
* 解决国内因不同发版而造成的UA数据不一致: 例如很多机型会因同电信、移动、联通而UA信息不同，但实际应该把他们算成同一款手机
* 解决机型的重命名与合并: 很多手机在不同时间生产其UA信息可能不同，所以需要对他们进行合并，防止在展示top数据时因数据分散而排不上号。

## 解析成功率
供参考（以30000个线上ua测试）:
* 浏览器：98.5%
* 系统： 99.8%
* 内核： 99.92%
* 设备类型： 100%
* 设备型号：98.9%
* 厂商信息：87.2%

## javascript版本
[ua-device](https://github.com/fex-team/ua-device)


## 安装

```bash
pip install -U uaDevice
```

## 使用

```python
import uaDevice
ua='Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 MQQBrowser/8.9.1 Mobile/15E148 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1'
info = uaDevice.parseUA(ua)
output = '\t'.join([
    info['os']['name'],
    info['os']['version']['original'],
    info['browser']['name'],
    info['browser']['version']['original'],
    info['engine']['name'],
    info['engine']['version']['original'],
    info['device']['type'],
    info['device']['model'],
    info['device']['manufacturer']
])
print(output)
```

## 贡献
随着新设备新app等等的上市，ua信息会越来越复杂，因为该项目需要不断迭代，希望大家一起来贡献不支持的ua，使得ua解析越来越准确

## 感谢
该项目是基于fex团队维护的js版本的ua解析库[ua-device](https://github.com/fex-team/ua-device)， 在此表示感谢