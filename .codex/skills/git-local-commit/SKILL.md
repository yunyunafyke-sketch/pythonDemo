---
name: git-local-commit
description: 根据当前对话上下文和 Git 实际改动，识别最近未提交内容并静默完成一次本地 commit（不 push）。当用户要求“提交当前改动”“帮我本地 commit”“把本轮修改提交一下”或类似诉求时使用。若本对话中已经提交过，则从当前工作区断点继续，只提交新的未提交内容。

---

# Git Local Commit 本地 Git 提交

## Commit Message 中文规范

### Commit Message 格式

统一采用：

<类型>: <中文描述>

例如：

feat: 新增账号状态管理功能
fix: 修复员工导出空指针异常
refactor: 重构应用导航查询逻辑
docs: 补充接口设计文档
test: 增加账号有效性校验测试
chore: 调整配置项命名规范
perf: 优化导出任务查询性能
style: 统一代码格式

### 类型规范

仅允许使用以下前缀：

feat
fix
refactor
docs
test
chore
perf
style

### 中文规范

- 类型前缀允许使用英文规范。
- 描述部分必须使用简体中文。
- 不允许生成纯英文提交信息。
- 不允许中英混写。
- 优先描述业务价值，而非技术动作。
- 禁止生成 update、modify、changes、fix bug 等无意义提交信息。

正确示例：

feat: 新增忘记密码验证码发送功能
feat: 新增账号启用停用接口
fix: 修复模板导入文件名未保存问题
fix: 修复区域编码查询条件错误
refactor: 重构应用导航领域服务实现

错误示例：

feat: add account api
fix: update export logic
refactor: optimize code
update code
fix bug
modify files
changes

### Message 生成规则

生成 commit message 时优先结合：

1. 当前对话上下文
2. git diff 实际改动
3. 修改文件名称
4. 最近一次 commit 内容

推断本次改动的真实业务含义。

要求：

- 说明做了什么业务功能。
- 不描述编辑动作。
- 不描述文件操作。
- 不描述开发过程。
- 不使用模糊表述。

### 约束补充

- Commit Message 必须使用中文描述。
- 类型前缀允许使用英文规范（feat/fix/refactor/docs/test/chore/perf/style）。
- 描述部分禁止使用英文。
- 优先描述业务功能或业务问题，而非代码修改动作。
- 若能够从上下文推断业务目标，则使用业务语义生成提交信息。
- 若无法确定业务目标，则根据 git diff 推断最准确的中文描述。
