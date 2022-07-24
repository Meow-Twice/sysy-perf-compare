# SysY 性能比较工具

给出两份由 [评测程序](https://github.com/Meow-Twice/sysy-test) 生成的 json 格式评测结果，对比这两份结果的性能差异。

## 使用说明

需要安装 `prettytable` 库: 

```shell
pip install prettytable -i https://pypi.tuna.tsinghua.edu.cn/simple
```

假设两份性能测试评测结果分别为 `result1.json` 和 `result2.json` ，则使用如下命令运行:

```shell
python3 -u perf.py result1.json result2.json
```

性能比较结果直接输出到控制台，比对的范围是两份结果中同时包含的测试点(测试集名称和测试用例名称均一致)。