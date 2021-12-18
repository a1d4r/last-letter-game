import time

from node import MyOwnPeer2PeerNode

node_1 = MyOwnPeer2PeerNode("127.0.0.1", 8001)
node_2 = MyOwnPeer2PeerNode("127.0.0.1", 8002)
node_3 = MyOwnPeer2PeerNode("127.0.0.1", 8003)

time.sleep(1)

node_1.start()
node_2.start()
node_3.start()

time.sleep(1)

node_1.connect_with_node('127.0.0.1', 8002)
node_2.connect_with_node('127.0.0.1', 8003)
node_3.connect_with_node('127.0.0.1', 8001)

time.sleep(2)

node_1.send_to_nodes({ "name" : "Maurice", "number" : 11 })

time.sleep(5)

node_1.stop()
node_2.stop()
node_3.stop()
print('end test')
