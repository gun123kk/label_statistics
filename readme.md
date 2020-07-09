
找出新增label並統計與排名
===
流程圖
---

1.比對找出新增的label資料




![](https://i.imgur.com/JnsRGLL.png)


2.統計與排名


匯出結果如下
(1)result_table_rank_by_file.csv
(2)result_table_rank_by_person.csv
若是只單純要統計與排名資料也可將檔案（*.json or *.csv）直接放在./rsfile/底下

![](https://i.imgur.com/ozsSSRP.png)











比對架構
---
（!!!必需更換或改進比對演算法,目前執行非常耗時！！） 
![](https://i.imgur.com/DCjvFHL.png)
![](https://i.imgur.com/Ab2EzZV.png)




執行步驟
---
```gherkin=
1.比對找出新增的label資料
若為.csv檔案,請執行以下步驟：
$ cd compare_csv_data 
 將原始資料放入org_file(請參考gitgub上的範例檔案,並按照資料夾與資料名稱分門別類）

執行比對
$ python3 compare_csv.py 20
20為要比對的Drone_020名稱,請依照要比對的檔案輸入名稱


若為.json檔案,請執行以下步驟：
$ cd compare_ex_json_data
 將原始資料放入org_file(請參考gitgub上的範例檔案,並按照資料夾與資料名稱分門別類）

執行比對
$ python3 compare_ex_json.py 49
49為要比對的Drone_049名稱,請依照要比對的檔案輸入名稱

執行以上步驟,若是執行後沒有任何錯誤,會產生.csv檔案,並將結果放到下列兩個路徑
(1)./result
(2)../cfile/


```

```gherkin=
2.統計與排名
若1執行完畢,請執行以下步驟獲得統計與排名資訊
$ cd ..
$ python3 main.py 1
1為選擇cfile之路徑,也就是要將執行比對後的檔案進行統計與排名
若輸入0,如下表示,則代表直接使用統計與排名功能,不做任何比對
$ python3 main.py 0

若是步驟2執行後沒有任何錯誤,會產生統計表csv檔案兩份,輸出如下
(1)result_table_rank_by_file.csv （依照label數量排名,不理會是否為同一人增加的,也就是說同一人可能會有不同名次）
(2)result_table_rank_by_person.csv　（依照label數量排名,但若同一人修改兩份以上之檔案,排名會將其整合在一塊）
```
