#

. ./cmd.sh
. ./path.sh
set -e

userpath=`pwd`/userdata/$1

model=model/xvector_nnet_1a

stage=0

if [ $stage -le 1 ]; then
    # get utt2spk and spk2utt file for username data
    
    utils/utt2spk_to_spk2utt.pl $userpath/data/utt2spk > $userpath/data/spk2utt || exit 1
    utils/spk2utt_to_utt2spk.pl $userpath/data/spk2utt > $userpath/data/utt2spk || exit 1
    
    # sorted spk2utt, fix_data_dir start on
    utils/fix_data_dir.sh $userpath/data
fi

if [ $stage -le 2 ]; then
    # Make MFCCs and compute the energy-based VAD for each dataset
    steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
    $userpath/data $userpath/log $userpath/feat
    
    utils/fix_data_dir.sh $userpath/data
    
    # compute vad decision, VAD start on
    sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
        $userpath/data $userpath/log $userpath/feat
    utils/fix_data_dir.sh $userpath/data
fi

if [ $stage -le 3 ]; then
  # Extract x-vectors used in the evaluation.
  sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd" --nj 1 \
    $model $userpath/data \
    $userpath/model
fi 
