# pdf-utils

功能：在 pdf 文档的最后一页，加入透明背景的 png 图片

运行：

1. 需要 python 环境，此处不详述。

2. 运行 init.sh，初始化目录结构。目录含义：

   - img-raw: 待处理图片

   - pdf-raw: 待处理 pdf

   - target: 拼接产物

   将你的文件放入指定目录中。

3. 运行 python merge.py，拼接好的 pdf 将存储在 target 目录下。

Enjoy it  : )