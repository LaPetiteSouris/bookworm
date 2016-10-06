import os

NEO4J_HOST = os.getenv('NEO4J_HOST', 'localhost')
NEO4J_PORT = int(os.getenv('NEO4J_PORT', 7474))
NEO4J_USER = os.getenv('NEO4J_USER', '')
NEO4J_PWD = os.getenv('NEO4J_PWD', '')

URI = os.getenv('NEO4J_URI',
                'http://bookworm_graph:ipbmX4LiLDcLHpM77RYX@hobby-knhkoomjfhocgbkeonmkpenl.dbs.graphenedb.com:24789/db/data/')
