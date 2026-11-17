# 场景与证据格式

目录可以遵循项目约定。下面是足够支撑第一版循环的最小形式，不需要每个项目搭建新的测试框架。

```text
<证据目录>/
  scenes.md                固定场景：步骤、输入、滚动目标、数据前提
  round-00/                基线
    screenshots.json
    01-desktop.png
    02-mobile.png
    review.md
  round-01/                原场景修复后；后续版本以此类推
    screenshots.json
    01-desktop.png
    02-mobile.png
    review.md
  report.md                处理记录、功能验证、结论和边界
```

不必创建空目录/空报告。瞬态图在同轮用单独 ID，例如 `mobile-results-loading`，稳定场景不得被瞬态替代。

## 截图清单

每轮清单引用图片路径，**相对于清单所在目录**，也支持本地绝对路径；不支持远程 URL。

```json
{
  "schema_version": 1,
  "round": "round-00",
  "screenshots": [
    {
      "scene_id": "desktop-overview",
      "file": "01-desktop.png",
      "viewport": [1440, 900],
      "capture": "viewport",
      "locale": "en",
      "state": "首屏；无搜索；无弹层"
    },
    {
      "scene_id": "mobile-results",
      "file": "02-mobile.png",
      "viewport": [390, 844],
      "capture": "viewport",
      "locale": "zh",
      "state": "筛选后的第一条结果；按 scenes.md 的步骤恢复"
    }
  ]
}
```

`scene_id` 在一轮内唯一，跨轮保持不变。`capture` 为 `viewport` 或 `full-page`。只有实际存在的必测图进入本轮清单；未完成的必测场景在报告显式列出，不得通过删清单条目掩盖缺测。

`verify_screenshots.py` 支持 PNG/JPEG/WebP，使用 Python 3 标准库。它校验文件、格式、ID、视口宽高比，输出像素尺寸、SHA-256 与重复图警告。允许浏览器排除滚动条/同比缩放，不要求像素精确等于视口。全页图不按视口高度比较；不支持的格式需转用浏览器支持的截图格式，不能靠改后缀冒充。

```bash
python3 <skill目录>/scripts/verify_screenshots.py round-01/screenshots.json --output round-01/verification.json
```

退出码：0 为元数据检查通过（可能有警告），1 为证据有问题，2 为输入/调用错误。默认宽高比相对误差阈值 3%，可用 `--ratio-tolerance` 调整；比例通过仍需人工检查内容。脚本不证明图片可解码、图片是否拍对或功能通过。

## 问题与最终报告

每个问题至少保留：稳定编号、场景/版本、级别、位置、现象/影响、主 Agent 核实结果、处理或不处理理由、对应复查图片、当前状态。采集疑点重新截图确认；不能把未解决问题改名为偏好来收口。

最终报告记录：

- 本轮范围和基线，哪些模板被修改、哪些检查后无需修改；
- 固定场景及覆盖表，逐轮原始意见与处理结果；
- 前后截图及剩余 P2；未显示/未执行/失败的检查；
- 功能回归命令、实际结果及既有跳过原因；
- 分开记录视觉结论和本轮请求完成度：只读审阅可以交付完成，同时说明功能未验证；完整修复任务未完成回归时不得称整体验收通过。不把模板抽样扩大为每个生成页面通过；
- 只有实际发布时才记录发布提交、构建、版本/流量及线上回读。
