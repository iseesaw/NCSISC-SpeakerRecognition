<center>
    <img src="process.png" height="70%" width="70%">
</center>

```
.
|-- README.md
|-- audios
|   |-- text
|   `-- wav
|-- construct.md
|-- enroll.py        // 预处理注册 call xvector/enroll.sh
|-- forced_align     // 强制对齐, 提取textgrid
|   |-- README.md
|   |-- numbers.txt
|   `-- trans.py
|-- login.py         // 预处理登录 call xvector/login.sh
|-- process.png
|-- userdata         // 用户注册向量模型
|   |-- user1
|   `-- user2
`-- xvector
    |-- cmd.sh
    |-- conf
    |-- enroll.sh    // 处理utt2spk/2utt, 提取MFCC特征以及xvector向量保存到userdata/user#
    |-- exp
    |-- generate.py  // ...
    |-- local
    |-- login.sh     // 处理utt2spk/2utt, 提取MFCC特征集xvector向量并进行plda得分计算
    |-- path.sh
    |-- prepare.py   // 生成待处理语音utt2spk, spk2utt
    |-- score.py     // 解析score文件返回结果
    |-- sid
    |-- steps
    `-- utils
```
12 directories, 17 files
