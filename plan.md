### 开发计划

#### 0.6.1.dev (2024/4/17 ~ 2024/7/1)

- 设置界面迁移，从顶部点击按钮弹出菜单界面，点击其中的设置按钮弹出（dialog / widget）。
- ADB 界面迁移，从顶部点击按钮弹出菜单界面，点击其中的 ADB 按钮弹出（dialog / widget）。
- 签名配置界面迁移，从顶部点击按钮弹出菜单界面，点击其中的签名配置按钮弹出（dialog / widget）。


最终发版： 2024/7/2


#### 0.6.2.dev (2024/7/1 ~ 2024/9/5)


- 多线程使用 QThreadPool，单个任务定为一个 worker, 任务中的具体步骤定为一个 stepTask。
- 优化 stepTask 执行的 loading UI，状态分为 执行前，执行中，执行成功，执行失败。

最终发版： 2024/9/6

#### 0.6.3.dev (2024/9/6 ~ 2024/11/5)

- 检查更新 + 登录。