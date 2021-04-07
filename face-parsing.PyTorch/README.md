# face-parsing.PyTorch

modified [face-parsing.PyTorch](https://github.com/zllrunning/face-parsing.PyTorch) to get the face parsing
for this project ([ca-gan](https://github.com/jehovahxu/ca-gan))

### Demo
- you need download [their pre-trained model](https://drive.google.com/open?id=154JgKpzCPW82qINcVieuPH3fZ2e0P812) and save it in `res/cp`
- Evaluate the trained model using:
    ```shell script
    # evaluate using GPU
    python test.py
    ```
- get face parsing mat
    ```shell script
    python test_save_mat.py
    ```
  you can modify the argparse parameter such as `--inputPath` and `--savePath` to generate the mat

### Reference
- [CelebAMask-HQ dataset](https://github.com/switchablenorms/CelebAMask-HQ) 
    
    Mask labels are defined as following:
    
    | Label list | | |
    | ------------ | ------------- | ------------ |
    | 0: 'background' | 1: 'skin' | 2: 'nose' |
    | 3: 'eye_g' | 4: 'l_eye' | 5: 'r_eye' |
    | 6: 'l_brow' | 7: 'r_brow' | 8: 'l_ear' |
    | 9: 'r_ear' | 10: 'mouth' | 11: 'u_lip' |
    | 12: 'l_lip' | 13: 'hair' | 14: 'hat' |
    | 15: 'ear_r' | 16: 'neck_l' | 17: 'neck' |
    | 18: 'cloth' | | |
- [face-parsing.PyTorch](https://github.com/zllrunning/face-parsing.PyTorch) 
    
    here you can see more details for train and test a face parsing model 
- [BiseNet](https://github.com/CoinCheung/BiSeNet)