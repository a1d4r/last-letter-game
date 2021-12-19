from typing import Optional

import typer

from .node import GamePeerNode

app = typer.Typer()


@app.command()
def main(
    host: str = "127.0.0.1",
    port: int = 1234,
    name: Optional[str] = None,
    redis_dsn: str = "redis://127.0.0.1:6379/0",
) -> None:
    node = GamePeerNode(host=host, port=port, redis_dsn=redis_dsn, id=name)
    # node.connect_with_node("127.0.0.1", 1234)
    try:
        node.start()
        while True:
            word = input()
            if word == "exit":
                node.stop()
                return
            node.move_to_next_player()
            node.send_to_nodes(word)
    finally:
        node.stop()
