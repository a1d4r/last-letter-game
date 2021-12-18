from p2pnetwork.node import Node
from loguru import logger


class MyOwnPeer2PeerNode(Node):
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super().__init__(host, port, id, callback, max_connections)
        logger.debug("MyPeer2PeerNode: Started")

    def outbound_node_connected(self, connected_node):
        """
        The node connects with another node - node.connect_with_node('127.0.0.1', 8002) -
        and the connection is successful. While the basic functionality is to exchange
        the node id's, no user data is involved.
        """
        logger.debug("outbound_node_connected: " + connected_node.id[:5])

    def inbound_node_connected(self, connected_node):
        """
        Another node has made a connection with this node and the connection is successful.
        While the basic functionality is to exchange the node id's, no user data is involved.
        """
        logger.debug("inbound_node_connected: " + connected_node.id[:5])

    def outbound_node_disconnected(self, connected_node):
        """
        A node, to which we had made a connection in the past, is disconnected.
        """
        logger.debug("outbound_node_disconnected: " + connected_node.id[:5])

    def inbound_node_disconnected(self, connected_node):
        """
        A node, that had made a connection with us in the past, is disconnected.
        """
        logger.debug("inbound_node_disconnected: " + connected_node.id[:5])

    def node_message(self, connected_node, data):
        """
        A node - connected_node - sends a message. At this moment the basic
        functionality expects JSON format. It tries to decode JSON when the message is received.
        If it is not possible, the message is rejected.
        """
        logger.debug("node_message from " + connected_node.id[:5] + ": " + str(data))

    def node_disconnect_with_outbound_node(self, connected_node):
        """
        The application actively wants to disconnect the outbound node, a node with which
        we had made a connection in the past. You could send some last message to the node,
        that you are planning to disconnect, for example.
        """
        logger.debug("node wants to disconnect with other outbound node: " + connected_node.id[:5])

    def node_request_to_stop(self):
        """
        The main node, also the application, is stopping itself.
        Note that the variable connected_node is empty, while there is no connected node involved.
        """
        logger.debug("node is requested to stop!")

    # OPTIONAL
    # If you need to override the NodeConection as well, you need to
    # override this method! In this method, you can initiate
    # you own NodeConnection class.
    # def create_new_connection(self, connection, id, host, port):
    #     return MyOwnNodeConnection(self, connection, id, host, port)
