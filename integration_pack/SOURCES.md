# 来源与补齐方式

## 上游项目

- CopilotKit: https://github.com/CopilotKit/CopilotKit
- Wimoor ERP: https://github.com/wimoor-erp/wimoor
- Wimoor 文档站: https://wiki.wimoor.com
- CopilotKit 文档: https://docs.copilotkit.ai
- AG-UI 协议: https://docs.ag-ui.com

## 本地获取状态

尝试克隆以下仓库时，本地命令行网络被阻断：

```powershell
git clone --depth 1 https://github.com/wimoor-erp/wimoor.git .sources/wimoor
git clone --depth 1 https://github.com/CopilotKit/CopilotKit.git .sources/CopilotKit
```

因此当前整合包没有直接复制上游源码文件，而是先整理了：

- 可确认的模块目录和源码清单
- 广告投放域的接口契约
- CopilotKit 接入模式
- 后续融合到 agent 项目的实施蓝图

## 网络恢复后的源码补齐流程

在工作区根目录执行：

```powershell
.\integration_pack\fetch_sources.ps1
```

这个脚本会：

- 克隆 Wimoor 和 CopilotKit 到 `.sources/`。
- 复制 `wimoor-amazon-adv` 到 `integration_pack/wimoor-advertising/source/`。
- 复制 Wimoor 广告模块可能依赖的 `pom.xml`、`wimoor-common`、`wimoor-system`、`wimoor-amazon`。
- 复制 CopilotKit 的 `packages`、`examples`、`docs` 和包管理入口到 `integration_pack/copilotkit-agent-ui/source-reference/`，用于后续 agent UI 融合参考。

CopilotKit 建议后续不要复制整个 monorepo，而是在目标前端项目中通过包管理器安装，并只参考 `packages`、`examples`、`docs` 中与 agent UI 相关的代码。
