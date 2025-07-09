# PySide6 Application Template

- 💡本项目是一个模板仓库，目的是为了更便捷地开发带有用户界面的小工具。

- 📓项目依赖:

    - Python>=3.12
    - PySide6-Essentials==6.9.1
    - PySide6-Fluent-Widgets==1.8.3
    - rich==14.0.0
    - pyinstaller==6.14.2

- ⚙️项目全部配置文件均放置在 `config` 下，包括开发依赖 `requirements.txt` 和运行配置 `config.json`，
`config.json` 运行配置在打包时会被正确包含到包内。

- 📦项目打包方式是 `pyinstaller`，打包时直接执行 `python pyinstaller.py`。

- 🖼️`assets` 中存放项目的静态资源，例如图标等。

- 🛠️`init_dev_env.sh` 用于初始化开发环境，主要是初始化 `venv` 环境、激活环境、安装 `requirements.txt` 中配置的依赖、配置 `.git/info/exclude` 中的文件黑名单（懒得配置 `.gitignore`，但是也会包含一个 `.gitignore` 文件）。