VeighNa CTP 接口 macOS 部署指南（精炼版）
一、编译环境准备（一次性配置）
# 1. 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# 2. 安装 Xcode Command Line Tools（Python 编译依赖核心）
sudo xcode-select --install
sudo xcode-select --reset
# 3. 安装 GCC 兼容层（兜底编译工具）
brew install gcc
# 4. 验证环境
clang --version   # Apple Clang
gcc --version     # Homebrew GCC
make --version


二、vnpy_ctp 安装（关键：版本锁定）
⚠️ 核心原则
项目	要求	原因	
vnpy_ctp 版本	锁定 6.7.7.2	最新版 API 变更频繁，与 SimNow 环境不兼容	
vnpy 核心	使用最新版	向后兼容	
安装命令
# 卸载旧版
pip uninstall vnpy_ctp -y
# 锁定安装 6.7.7.2 版本
pip install git+https://github.com/vnpy/vnpy_ctp.git@6.7.7.2


三、源码替换与 macOS 适配（核心步骤）

3.1 获取 aitrados_ctp 源码
项目	信息	
来源	PyPI: aitrados-ctp	
版本	0.0.7	
下载地址	https://pypi.org/project/aitrados-ctp/	
下载文件	aitrados_ctp-0.0.7.tar.gz	
# 解压后目标文件路径
aitrados_ctp-0.0.7/vnpy_ctp/gateway/ctp_gateway.py
3.2 替换虚拟环境中的文件
# 1. 找到 vnpy_ctp 安装位置
pip show vnpy_ctp | grep "Location"
# 输出示例: /Users/leo/.venv/lib/python3.14/site-packages
# 2. 将 aitrados_ctp 的 ctp_gateway.py 复制覆盖到：
{Location}/vnpy_ctp/gateway/ctp_gateway.py


3.3 macOS 适配修改（必须）
修改点 1：CtpMdApi.connect 方法
def connect(self, address: str, userid: str, password: str, 
            brokerid: str, production_mode: bool) -> None:
    """连接服务器"""
    self.userid = userid
    self.password = password
    self.brokerid = brokerid
    if not self.connect_status:
        path: Path = get_folder_path(self.gateway_name.lower())
        # --- macOS 适配修改 ---
        self.createFtdcMdApi(str(path) + "/Md")  # ✅ 路径改为 /Md，字符串类型
        # ----------------------
        self.registerFront(address)
        self.init()
        self.connect_status = True



修改点 2：CtpTdApi.connect 方法
def connect(self, address: str, userid: str, password: str, 
            brokerid: str, auth_code: str, appid: str, 
            production_mode: bool) -> None:
    """连接服务器"""
    self.userid = userid
    self.password = password
    self.brokerid = brokerid
    self.auth_code = auth_code
    self.appid = appid
    if not self.connect_status:
        path: Path = get_folder_path(self.gateway_name.lower())
        # --- macOS 适配修改 ---
        self.createFtdcTraderApi(str(path) + "/Td")  # ✅ 路径改为 /Td，字符串类型
        # ----------------------
        self.subscribePrivateTopic(0)
        self.subscribePublicTopic(0)
        self.registerFront(address)
        self.init()
        self.connect_status = True
    else:
        self.authenticate()
修改对照表
原代码特征	macOS 修改	
...\\Md 或 ...\\Td	改为 /Md、/Td（正斜杠）	
.encode("GBK") 或 .encode()	移除，直接传 str	
production_mode 参数传递到底层 C++	移除该参数	


四、验证测试
# 无需重新安装，直接运行测试脚本
python test_ctp.py
# test_ctp.py
import time
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import SubscribeRequest
from vnpy.trader.constant import Exchange
from vnpy_ctp import CtpGateway
SETTING = {
    "用户名": "your_username",
    "密码": "your_password", 
    "经纪商代码": "9999",
    "交易服务器": "182.254.243.31:30001",
    "行情服务器": "182.254.243.31:30011",
    "产品名称": "simnow_client_test",
    "授权编码": "0000000000000000",
    "柜台环境": "模拟",
}
def event_handler(event: Event):
    if event.type in ["eTimer", "eContract"]:
        return
    print(f"[事件] {event.type}")
    if "Log" in event.type:
        print(f"  >>> {event.data.msg}")
def main():
    ee = EventEngine()
    me = MainEngine(ee)
    me.add_gateway(CtpGateway)
    ee.register_general(event_handler)
    me.connect(SETTING, "CTP")
    time.sleep(6)
    req = SubscribeRequest(symbol="rb2505", exchange=Exchange.SHFE)
    me.subscribe(req, "CTP")
    time.sleep(15)
    me.close()
    ee.stop()
if __name__ == "__main__":
    main()


五、流程速查
步骤1: 环境准备 → Homebrew + Xcode Tools + GCC
步骤2: 锁定安装 → pip install vnpy_ctp@6.7.7.2
步骤3: 获取源码 → 下载 aitrados_ctp-0.0.7.tar.gz
步骤4: 文件替换 → 覆盖 site-packages 中的 ctp_gateway.py
步骤5: 代码修改 → 路径改 /Md /Td，移除 encode
步骤6: 测试验证 → 运行 test_ctp.py


六、常见问题
问题	                         原因	                                    解决	
TypeError / unknown type name	vnpy_ctp 版本错误	                      重新安装 6.7.7.2	
路径错误	                     Windows 风格路径 \\	                    改为 macOS 风格 /	
编码错误	                     传递 bytes 给底层 C++	                    移除 .encode()	
连接失败	                     SimNow 7x24 时间段不符	                    确认测试时间段