### mandarian
声学模型

## g2p模型
### mandarian_character_g2p
g2p模型

### CH
g2p模型 mandarian_pinyin_g2p  
性能更好

### train mandarin g2p model
拼音词典 -> g2p模型
bin/mfa_train_g2p /path/to/examples/chinese_dict.txt CH_test_model.zip

## 对齐
bin/mfa_train_and_align path/to/examples/CH  path/to/examples/chinese_dict.txt examples/aligned_output
工具 g2p模型 词典 输出

bin/mfa_align /path/to/librispeech/dataset /path/to/librispeech/lexicon.txt english ~/Documents/aligned_librispeech

bin/mfa_align corpus_directory dictionary_path acoustic_model_path output_directory
工具 数据集(.wav .lab) 词汇表 声学模型 输出