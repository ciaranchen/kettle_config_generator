## XML的空格问题

XML中空格是不能忽略的，最初写`parse.py`时忽略了这个问题，导致很多失误。

## XML的字符编码问题

理论上来说，一个理想的XML配置文件，除了字段名和tag左右的书名号外，不应该有其它的书名号，因此如果在其中的SQL语句有大于小于符号的时候，应该对代码进行重新的修改。

只是在这个项目中没有考虑这一点而已。
