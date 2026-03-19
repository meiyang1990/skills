---
name: current-dir
description: Provide and use the current working directory of the user environment. Use when the user asks for the current path, workspace location, or where shell commands are being executed.
---

# Current Directory

## 作用

- 帮助准确获取并说明当前工作目录（current working directory）
- 在需要执行与路径相关的命令时，选择合适的方式获取目录信息

## 适用场景

- 用户提问“当前目录是什么”“现在在什么路径”“工程在哪个目录”等
- 需要说明命令是在什么目录下执行
- 需要确认项目根目录或 git 仓库根目录

## 使用原则

1. **不要凭空猜测路径**  
   - 优先使用系统或工具提供的“工作区根路径”信息（如果系统提示了当前 workspace/root）
   - 如仍不确定，再调用 Shell 获取

2. **获取当前 shell 工作目录（CWD）**
   - 在需要精确当前 shell 目录时，调用 Shell 执行：
     - `pwd`
   - 只在与路径、文件位置或命令执行位置强相关时才调用，避免无意义调用

3. **获取项目根目录（Git 仓库场景）**
   - 如果当前是在 git 仓库中，且需要项目根目录，可调用：
     - `git rev-parse --show-toplevel`
   - 在回答中明确说明这是“git 仓库根目录”

4. **回答用户时的说明方式**
   - 清晰区分不同概念：
     - “当前 shell 工作目录”（`pwd` 返回值）
     - “项目根目录 / 仓库根目录”（如 `git rev-parse --show-toplevel` 返回值）
   - 用简洁中文说明路径，例如：
     - “当前工作目录是：\`/path/to/dir\`”
     - “当前 git 仓库根目录是：\`/path/to/repo\`”

5. **路径相关建议**
   - 给出与路径相关的命令时，尽量使用绝对路径或清楚标注“在某目录下执行”
   - 避免使用 Windows 风格路径，只使用类似 `a/b/c` 的形式

## 简要流程（供内部参考）

1. 用户提到“当前目录/路径/在哪执行命令”等 → 认为应使用本 skill
2. 若系统已给出 workspace 或项目根路径 → 直接基于该信息回答
3. 若需要更精确的 shell 目录 → 调用 Shell 执行 `pwd`
4. 若用户关心 git 仓库根目录 → 调用 `git rev-parse --show-toplevel`
5. 用清晰简洁的中文向用户说明目录信息，并在需要时给出下一步操作建议

