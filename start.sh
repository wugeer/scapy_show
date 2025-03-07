#!/bin/bash
set -e

# 启动Ray Serve
python jieba_serve.py --host 0.0.0.0


# 如果Ray Serve退出，脚本也退出

