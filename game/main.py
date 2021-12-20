import sys
from typing import Optional

import typer
from loguru import logger

from .node import GamePeerNode

app = typer.Typer()


@app.command()
def main(
    host: str = "127.0.0.1",
    port: int = 1234,
    name: Optional[str] = None,
    redis_dsn: str = "redis://127.0.0.1:6379/0",
    debug: bool = typer.Option(False, "--debug"),
) -> None:
    if not debug:
        logger.remove()
        logger.add(sys.stdout, level="INFO")
    node = GamePeerNode(host=host, port=port, redis_dsn=redis_dsn, id=name)
    try:  # pylint: disable=too-many-nested-blocks
        node.start()
        while True:
            word = input()
            while not node.is_word_valid(word):
                if word[0].lower() != node.last_letter:
                    logger.error(f"Word should starts with letter {node.last_letter}")
                else:
                    logger.error("This word has already been used. Try another word.")
                word = input()

            node.move_to_next_player()
            node.add_word(word)
            node.send_to_nodes(word)
            logger.debug(node.words)
    finally:
        node.stop()
