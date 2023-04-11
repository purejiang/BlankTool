# BlankTool-v4

## 简介：
基于 PySide6 开发的桌面应用，集合了各种 Android 开发的功能，通过应用化的 UI 简化了各种工具的使用。


## 说明：

### 工具
- apktool-2.7.0
- bundletool-1.11.0
- aapt2
- adb
### 环境
- jre-11
- python-3.9.12

项目现已自带以上工具和环境，无需配置。
### 功能
- 已包含的功能
  - apk / aab 的安装
  - apk 的解析、反编译、重编译、重签
  - 全局的签名配置

- 正在开发的功能：
  - 缓存清理和日志开启设置
  - 获取手机上已安装的 apk 列表 + 提取
  - apk 转 aab

- 未来规划的功能
  - aab 解析
  - aab 的 assets 资源分割
  - apk、aab 方法数统计
  - apk、aab 签名信息的提取
  - FB开发散列的获取\
...

### 项目结构
- [cache](./cache) （缓存目录）
  - [aab](./cache/aab)（aab功能的缓存目录）
  - ...
- [common](./common)（常量）
- [config](./config)（应用配置，开发人员使用）
- [data](./data)（使用过程中产生的本地数据）
- [logic](./logic)（功能类）
- [re](./re)（环境+工具）
- [res](./res)（资源文件，图片、.ui、.qss）
- [utils](./utils)（工具类）
- [viewmodel](./viewmodel)（操作类）
- [vo](./vo)（实体类）
- [widget](./widget)（界面+控件）
- [main.py](./main.py)（程序入口）
- [main.spec](./main.spec)（打包配置）
- [project2exe.py](./project2exe.py)（打包脚本，将项目打包成.exe）
- [requirements.txt](./requirements.txt)（依赖项）


.qss 文件作为风格配置。\
.ui 为控件和 UI 的显示文件。\
.py 加载 .ui + .qss 进行界面绘制，同时各个功能也都通过 .py 实现。




