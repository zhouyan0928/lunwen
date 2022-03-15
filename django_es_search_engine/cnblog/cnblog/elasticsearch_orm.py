from elasticsearch_dsl import Date, analyzer, Keyword, Text, Document
from elasticsearch_dsl.connections import connections                       # 导入连接elasticsearch(搜索引擎)服务器方法

connections.create_connection(hosts=['127.0.0.1'])

ik_analyzer = analyzer('ik_max_word')

class cnblogsType(Document):

    title = Text(analyzer="ik_max_word")
    description = Text(analyzer="ik_max_word")
    url = Keyword()
    riqi = Date()

    class Index:
        name = 'cnblogs'
        settings = {
            "number_of_shards": 5,
        }

es = connections.create_connection(cnblogsType)

if __name__ == '__main__':
    cnblogsType.init()