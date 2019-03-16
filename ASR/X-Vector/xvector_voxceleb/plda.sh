# 将数据按enroll和test切分(python读取enroll.json和test.json分别保存到data/enroll,test)
# 提取所有enroll、test数据x-vector(x-vector.ark转为x-vector.txt)
# 构造trials文件, 格式为 speaker/ uttr/ target or nontarget
# 计算plda score、计算eer
# 

. ./cmd.sh
. ./path.sh
set -e

trials=files/trials
enroll_dir=data/enroll/feat/xvectors_enroll_mfcc
test_dir=data/test/feat/xvectors_enroll_mfcc
nnet_dir=exp/xvector_nnet_1a

stage=0

if [ $stage -eq 0 ]; then
  $train_cmd exp/scores/log/enroll_test_scoring.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 $nnet_dir/xvectors_train/plda - |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:$enroll_dir/spk_xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:$test_dir/xvector.1.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "cat '$trials' | cut -d\  --fields=1,2 |" exp/scores_enroll_test || exit 1;

fi