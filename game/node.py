from typing import Any, Callable, Optional

import pottery
from loguru import logger
from p2pnetwork.node import Node
from redis import Redis


class GamePeerNode(Node):
    def __init__(
        self,
        host: str,
        port: int,
        redis_dsn: str,
        id: Optional[str] = None,
        callback: Optional[Callable[..., Any]] = None,
        max_connections: int = 0,
    ):
        super().__init__(
            host=host,
            port=port,
            id=id,
            callback=callback,
            max_connections=max_connections,
        )
        logger.debug(f"{self.host}:{self.port}")
        logger.info(f"You have joined the game as {self.id}")
        self._redis = Redis.from_url(redis_dsn)
        self._redis.ping()
        self.peers = pottery.RedisList([], redis=self._redis, key="peers")

        self.words = set()  # type: set[str]
        self.last_letter = None  # type: Optional[str]

        for peer in self.peers:
            logger.info(f"Connecting to {peer['id']}...")
            self.connect_with_node(peer["host"], peer["port"])
        self.peers.append(self.identity)

        self.current_player = pottery.RedisDict(redis=self._redis, key="current_player")

    @property
    def identity(self) -> dict[str, Any]:
        return {"host": self.host, "port": self.port, "id": self.id}

    def move_to_next_player(self) -> None:
        """
        Pass the move to the next player.
        """
        my_index = self.peers.index(self.identity)
        logger.debug(f"My index: {my_index}")
        self.current_player["index"] = (my_index + 1) % len(self.peers)

    def is_word_valid(self, word: str) -> bool:
        """
        Check if we can use specified word:
        1) It has not been used yet
        2) It starts with the last letter from the previous word.
        """
        return (self.last_letter is None) or (
            word not in self.words and word[0].lower() == self.last_letter
        )

    def add_word(self, word: str) -> None:
        self.words.add(word)

    def outbound_node_connected(self, node: Node) -> None:
        """
        The node connects with another node - node.connect_with_node('127.0.0.1', 8002) -
        and the connection is successful. While the basic functionality is to exchange
        the node id's, no user data is involved.
        """
        logger.info(f"Connected to {node.id}")

    def inbound_node_connected(self, node: Node) -> None:
        """
        Another node has made a connection with this node and the connection is successful.
        While the basic functionality is to exchange the node id's, no user data is involved.
        """
        logger.info(f"{node.id} joined the game.")

    def outbound_node_disconnected(self, node: Node) -> None:
        """
        A node, to which we had made a connection in the past, is disconnected.
        """
        logger.info(f"{node.id} left the game.")

    def inbound_node_disconnected(self, node: Node) -> None:
        """
        A node, that had made a connection with us in the past, is disconnected.
        """
        logger.info(f"{node.id} left the game.")

    def node_message(self, node: Node, data: str) -> None:
        """
        A node - connected_node - sends a message. At this moment the basic
        functionality expects JSON format. It tries to decode JSON when the message is received.
        If it is not possible, the message is rejected.
        """
        word = data.strip()
        self.last_letter = word[-1].lower()
        self.words.add(word)
        logger.info(f"{node.id} said: {word}.")

        current_player_identity = self.peers[self.current_player["index"]]
        if self.identity == current_player_identity:
            logger.info("Your turn: ")
        else:
            logger.info(f"{current_player_identity['id']}'s turn.")

    def node_disconnect_with_outbound_node(self, node: Node) -> None:
        """
        The application actively wants to disconnect the outbound node, a node with which
        we had made a connection in the past. You could send some last message to the node,
        that you are planning to disconnect, for example.
        """
        logger.debug("node wants to disconnect with other outbound node: " + node.id)

    def shutdown(self) -> None:
        logger.info("Shutting down...")
        self.peers.remove(self.identity)

    def node_request_to_stop(self) -> None:
        """
        The main node, also the application, is stopping itself.
        Note that the variable connected_node is empty, while there is no connected node involved.
        """
        logger.debug("Shutting down...")
        self.peers.remove(self.identity)

    # OPTIONAL
    # If you need to override the NodeConection as well, you need to
    # override this method! In this method, you can initiate
    # you own NodeConnection class.
    # def create_new_connection(self, connection, id, host, port):
    #     return MyOwnNodeConnection(self, connection, id, host, port)
