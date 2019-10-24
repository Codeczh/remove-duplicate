#remove-duplicate
---
#The image fingerprinting algorithm to remove duplicates of web set
---
###### Note: This code will delete repeat images!You may need to back up your data set.

If you want copy dataset, remember to uncomment the code in `gather.py`. 
>dataset =trainset[:trainset.rfind('\\')+1]+'train_delete'      
>copy_data(trainset,dataset)  

and comment 
>dataset =trainset

Then the `train` will be copied to `train-delete`

------

The directory path is as shown below:  
```python
 ---|------web-bird_ _ _ _ _ _ _ _ _ _train
    |                      | _ _ _ _ _val  
    |-----image-fingerprinting_ _ _ _gather.py  
                           |_ _ _ _ _move_repeat.py  
                           |_ _ _ _ _index.py  
```

Run ` gather.py ` to generate `repeat` folder, containing duplicate images, under `web-bird`.
Run `move_repeat.py` to move those repeat images intra sub-classes to `repeat_sub` under `web-bird` as well.

------------
reference:    
[cnblog中文翻译](https://www.cnblogs.com/wing1995/p/4471034.html)   
[web fine-grained 去重简介](http://note.youdao.com/noteshare?id=07d47b895298c58c6c0ffc11833741c8)
