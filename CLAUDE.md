# Atlas 协作约定

- 默认工作流：修改完成并通过校验后，直接提交、推送并合并到 `main`（通过 PR 合并即可，无需等待确认）；除非用户在当次请求中特别声明不要合并。
- 修改手册后运行 `python3 tools/check_handbook.py topics/<topic>`，须 0 失败再合并。
- 网站：`main` 每次更新由 `.github/workflows/pages.yml` 自动校验、构建（`tools/build_site.py` → `_site/`）并发布到 GitHub Pages：https://codebluce.github.io/Atlas/ 。全站索引 `catalog.html` 由 `topic.json` 生成，新增或变更模块后务必同步 `topic.json`。本地预览：`python3 tools/build_site.py && python3 -m http.server -d _site`。
