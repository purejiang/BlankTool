# BlankTool
[🇨🇳 中文文档](https://github.com/purejiang/BlankTool/blob/main/README_ZH.md)

The desktop application developed based on PySide6 integrates various Android development functions and simplifies the use of various tools through an applied UI.

## Introduce：

### Tool
- apktool-2.7.0
- bundletool-1.11.0
- aapt2
- adb
### Environment
- jre-11
- python-3.9.12


The project now comes with the above tools and environment, without the need for configuration.
### Functions
- Already included
  - install apk / aab
  - parse apk , depackage, repackage, re-sign
  - Global signature configuration
  - Cache Cleanup and Log Enable Settings
  - Obtain a list of installed apps on your phone, extract and search app

- Under development：
  - apk to aab
  - get FB development hashes

- Future planning 
  - parse aab
  - aab to apk
  - aab's assets split
  - get apk/aab 's all method counts
  - get signature information of aab\
...

### Project Structure
- [cache](./cache) 
  - [aab](./cache/aab)
  - ...
- [common](./common)
- [config](./config)
- [data](./data)
- [logic](./logic)
- [re](./re)
- [res](./res)
- [utils](./utils)
- [viewmodel](./viewmodel)
- [vo](./vo)
- [widget](./widget)
- [main.py](./main.py)
- [main.spec](./main.spec)
- [project2exe.py](./project2exe.py)
- [requirements.txt](./requirements.txt)

.qss style files.\
.ui ui files.\
.py function files.

