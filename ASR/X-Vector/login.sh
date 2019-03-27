. ./cmd.sh
. ./path.sh
set -e

userpath=`pwd`/userdata/$1

model=model/xvector_nnet_1a

trials=$userpath/score/trials

stage=0

if [ $stage -le 0 ]; then
    # get utt2spk and spk2utt file for login data
    
    utils/utt2spk_to_spk2utt.pl $userpath/attack/utt2spk > $userpath/attack/spk2utt || exit 1
    utils/spk2utt_to_utt2spk.pl $userpath/attack/spk2utt > $userpath/attack/utt2spk || exit 1
    
    # sorted spk2utt, fix_data_dir start on
    utils/fix_data_dir.sh $userpath/attack
fi

if [ $stage -le 1 ]; then
    # Make MFCCs and compute the energy-based VAD for each dataset
    steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
    $userpath/attack $userpath/log $userpath/feat
    
    utils/fix_data_dir.sh $userpath/attack
    
    # compute vad decision, VAD start on
    sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
        $userpath/attack $userpath/log $userpath/feat
    utils/fix_data_dir.sh $userpath/attack
fi

if [ $stage -le 2 ]; then
  # Extract x-vectors used in the evaluation.
  sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd" --nj 1 \
    $model $userpath/attack \
    $userpath/login
fi 

if [ $stage -le 3 ]; then
  $train_cmd userpath/log/login_scoring.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 $model/xvectors_train/plda - |" \
    "ark:ivector-subtract-global-mean $model/xvectors_train/mean.vec scp:$userpath/model/spk_xvector.scp ark:- | transform-vec $model/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean $model/xvectors_train/mean.vec scp:$userpath/login/xvector.scp ark:- | transform-vec $model/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "cat '$trials' | cut -d\  --fields=1,2 |" $userpath/score/login.scores || exit 1;
fi
