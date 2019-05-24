#### how to use this module

**First of all**: Install montreal-forced-aligner 



**You should establish audio data file like this**

enroll  [dir]

|----speaker1 [dir]

|     |----utter1.wav

|     |----utter1.lab

|     |...

|----....

|----TextGrid [dir]



login  [dir]

|----speaker1 [dir]

|     |----utter1.wav

|     |----utter1.lab

|----TextGrid [dir]



**Attention**:

1. utter.lab can be created by this module, so not necessary
2. remember to delete speaker [dir]  after the whole process
3. see dataset_example as a example



#### Step

0. if you don't have .lab and .TextGrid file, first use forced_align.py to create it 

   Usage: python3 forced_align.py [wavFileDir]

   wavFileDir: is the like the path of "speaker1" in the enroll example 

1. when enrollment, use enroll.py 

   python3 enroll.py \[username] [user_root_path]

   username: like the "speaker1" 

   user_root_path: like the path of "speaker1"

2. when login, use login.py 

   Usage: python3 login.py \[username] [wavFileDir]

   username: like the "speaker1"

   user_root_path: like the path of "speaker1"

   

   