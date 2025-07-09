#!/bin/bash

PY_REQ_TXT=./config/requirements.txt
VENV_ROOT=./.venv
DOT_GIT_FILE=./.git
DOT_GIT_EXCLUDE_LIST=(
    "__pycache__"
    ".history"
    ".venv"
)

# create python virtual environment
if [ -d ${VENV_ROOT} ]; then
    echo "${VENV_ROOT} already exists"
else
    echo "Creating ${VENV_ROOT}"
    python -m venv ${VENV_ROOT}
fi

# activate venv
case "$OSTYPE" in
    linux-gnu)
        source ${VENV_ROOT}/bin/activate
        ;;
    *)
        source ${VENV_ROOT}/Scripts/activate
        ;;
esac

# update pip
python -m pip install --upgrade pip

# install dependencies
pip install -r ${PY_REQ_TXT}

# install certs
pip install pip-system-certs --use-feature=truststore
pip install --upgrade certifi

# 表驱动方式的核心修改
if [ -d "${DOT_GIT_FILE}" ]; then
    exclude_file="${DOT_GIT_FILE}/info/exclude"

    # 检查模式表中任意模式是否已存在
    found=0
    if [ -f "${exclude_file}" ]; then
        for pattern in "${DOT_GIT_EXCLUDE_LIST[@]}"; do
            if grep -qF "${pattern}" "${exclude_file}"; then
                found=1
                break
            fi
        done
    fi

printf -v joined '%s, ' "${DOT_GIT_EXCLUDE_LIST[@]}"
    if [ $found -eq 1 ]; then
        echo "git exclude already contains ${joined%, }"
    else
        echo  # 输出空行替代原echo -e "\n"

        # 使用表驱动方式添加排除项
        printf "%s\n" "${DOT_GIT_EXCLUDE_LIST[@]}" >> "${exclude_file}"

        # 格式化输出添加的项
        echo "Added ${joined%, } to git exclude"
    fi
fi