How to import Items.csv to Unit
sqlite3 db.sqlite3
sqlite> .mode csv
Remove the header raw from Items.csv
sqlite> .import Items.csv root_Item
sqlite> .tables
sqlite> select * from Item;
sqlite> .exit