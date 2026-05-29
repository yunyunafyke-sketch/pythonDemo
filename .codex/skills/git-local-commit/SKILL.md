---
name: git-local-commit
description: 根据当前对话上下文和 Git 实际改动，识别最近未提交内容并静默完成一次本地 commit（不 push）。当用户要求“提交当前改动”“帮我本地 commit”“把本轮修改提交一下”或类似诉求时使用。若本对话中已经提交过，则从当前工作区断点继续，只提交新的未提交内容。

---

# Git Local Commit 本地 Git 提交

## 目标

- 根据当前对话上下文和 `git status` / `git diff` 判断本轮实际修改了哪些文件。
- 优先只提交本轮对话相关改动；对明显无关的改动保持未提交状态。
- 为目标提交内容生成简洁准确的 commit message。
- 静默完成一次本地 `git commit`，不要求用户补充信息，除非存在明显会误提交的风险。
- 不执行 `git push`、不切换分支、不改写历史。

## 适用场景

当用户提出以下或类似诉求时，使用本 skill：

- “提交当前改动”
- “帮我本地 commit”
- “把本轮修改提交一下”
- “提交这次修改”
- “commit 一下，但不要 push”
- “把刚才改的代码提交到本地”

如果用户明确要求 push、切换分支、rebase、amend 或重写历史，本 skill 不自动扩展处理，只执行本地普通 commit 相关流程。

## 工作流

### 1. 建立断点和改动边界

先执行：

```bash
git status --porcelain
git branch --show-current
git log -1 --oneline
```

判断规则：

- 如果 `git status --porcelain` 为空：告知用户“当前没有新的未提交改动”，流程结束。
- 如果本对话中已经运行过本 skill 或类似 commit 流程：
  - 不使用 `--amend`。
  - 不重复处理已提交内容。
  - 以当前 `git status` 剩余内容作为新的断点继续提交。
- 如果当前分支信息获取失败，可以继续检查改动，但最终结果中说明分支识别失败。

### 2. 识别实际修改文件

执行：

```bash
git diff --name-status
git diff --cached --name-status
git diff --stat
```

处理规则：

- 未跟踪文件以 `git status --porcelain` 中的路径为准。
- 只在生成 commit message 必要时读取小文件内容。
- 不递归扫描无关目录。
- 不为了 commit 做额外重构、格式化或业务修改。
- 根据当前对话上下文，把改动分为：
  - 本轮相关改动
  - 明显无关改动
  - 无法判断边界的改动

提交边界规则：

- 如果能清楚区分：只提交本轮相关改动，明显无关改动保持未提交。
- 如果用户明确要求“提交剩余改动”“提交所有未提交内容”：以当前剩余工作区改动作为提交目标。
- 如果无法安全区分提交边界：先向用户确认，不要默认提交全部改动。
- 如果暂存区已有明显无关内容：不要直接提交，先向用户确认。

### 3. 生成 commit message

生成规则：

- 先看当前对话中完成的任务，再用实际文件列表和 diff 校正。
- message 应说明“做了什么”，不要只写 `update files`、`fix`、`changes` 等泛化内容。
- 如果对话上下文不足，直接根据文件改动生成 message，不因为缺少主题而打断用户。
- 优先使用一行 subject。
- 确有必要时，用第二个 `-m` 写 1 到 3 条简短正文。

示例：

```bash
git commit -m "fix: correct area code query SQL"
```

或：

```bash
git commit -m "feat: add async export task record" \
  -m "Create export record before async processing.\nKeep task status and file metadata traceable."
```

### 4. 执行本地提交

默认只暂存目标文件：

```bash
git add -- <目标文件路径...>
```

仅当用户明确要求提交当前全部剩余改动时，才执行：

```bash
git add -A
```

commit 前必须检查暂存内容：

```bash
git diff --cached --name-status
```

确认暂存内容符合本次提交目标后执行：

```bash
git commit -m "<总结后的 message>"
```

如果 `git add` 或 `git commit` 因 sandbox / 权限限制失败：

- 按当前执行环境允许的权限申请规则重试同一命令。
- 权限理由只需说明：`完成用户要求的本地 Git commit`。
- 不承诺绕过权限系统。

### 5. 返回提交结果

提交完成后，至少反馈：

- 当前分支名
- commit short hash
- 最终 commit message

可附加执行：

```bash
git show --stat --oneline -1
```

并反馈关键文件统计。

## 约束

- 不使用 `--amend`，除非用户明确要求。
- 不使用重置类破坏命令，例如 `git reset --hard`。
- 不执行 `git push`。
- 不切换分支。
- 不改写 Git 历史。
- 不创建文档、不改业务文件，只提交当前已有改动。
- 不把明显与本轮对话无关的改动混入提交。
- 若暂存区已有明显无关内容，不直接提交，先向用户确认。
- 只处理“当前未提交内容”的一次性本地提交，不扩展额外流程。

## 推荐回复格式

成功提交后：

```text
已完成本地 commit，未 push。

分支：<branch>
提交：<short-hash>
message：<commit-message>

提交内容：
<git show --stat --oneline -1 的关键信息>
```

没有改动时：

```text
当前没有新的未提交改动，无需 commit。
```

需要确认边界时：

```text
当前工作区存在无法确认是否属于本轮的改动，直接提交可能混入无关内容。
请确认要提交哪些文件：

<文件列表>
```
