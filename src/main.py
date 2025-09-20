"""Main MCP server implementation using FastMCP"""

import asyncio
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

from .games.registry import GameRegistry
from .games.types import GameAction

# Initialize FastMCP server
mcp = FastMCP("gym-mcp")

# Global registry instance
registry = GameRegistry()


@mcp.tool()
def list_games(show_active: bool = True) -> str:
    """List available game types and active game instances"""
    available_games = registry.get_available_games()
    result = {"available_games": available_games}

    if show_active:
        active_games = registry.get_active_games()
        result["active_games"] = active_games

    return f"Games: {result}"


@mcp.tool()
def start_game(game_type: str, players: List[str], game_id: Optional[str] = None) -> str:
    """Start a new game instance"""
    # Create game
    result = registry.create_game(game_type, game_id)
    if not result.success:
        return f"Error: {result.error}"

    # Start game with players
    game = registry.get_game(result.new_state.id)
    start_result = game.start(players)

    if start_result.success:
        return f"Game started: {start_result.new_state.model_dump()}"
    else:
        return f"Error starting game: {start_result.error}"


@mcp.tool()
def make_move(game_id: str, action_type: str, payload: Dict[str, Any], player: str) -> str:
    """Make a move in an active game"""
    game = registry.get_game(game_id)
    if not game:
        return f"Game {game_id} not found"

    action = GameAction(type=action_type, payload=payload, player=player)
    result = game.make_move(action)

    if result.success:
        return f"Move successful: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


@mcp.tool()
def get_game_state(game_id: str) -> str:
    """Get current state of a game"""
    game = registry.get_game(game_id)
    if not game:
        return f"Game {game_id} not found"

    state = game.get_state()
    return f"Game state: {state.model_dump()}"


@mcp.tool()
def reset_game(game_id: str) -> str:
    """Reset a game to initial state"""
    game = registry.get_game(game_id)
    if not game:
        return f"Game {game_id} not found"

    result = game.reset()
    if result.success:
        return f"Game reset: {result.new_state.model_dump()}"
    else:
        return f"Reset failed: {result.error}"


@mcp.tool()
def tic_tac_toe_place_mark(game_id: str, row: int, col: int, player: str) -> str:
    """Place a mark (X or O) on the tic-tac-toe board"""
    game = registry.get_game(game_id)
    if not game or game.type != "tic-tac-toe":
        return f"Tic-tac-toe game {game_id} not found"

    action = GameAction(
        type="place_mark",
        payload={"row": row, "col": col},
        player=player
    )
    result = game.make_move(action)

    if result.success:
        return f"Mark placed: {result.new_state.model_dump()}"
    else:
        return f"Failed to place mark: {result.error}"


# Gymnasium-specific tools
@mcp.tool()
def gym_step(game_id: str, action: Any, player: str) -> str:
    """Take a step in a Gymnasium environment"""
    game = registry.get_game(game_id)
    if not game:
        return f"Game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": action}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Step successful: {result.new_state.model_dump()}"
    else:
        return f"Step failed: {result.error}"


@mcp.tool()
def gym_reset(game_id: str) -> str:
    """Reset a Gymnasium environment"""
    game = registry.get_game(game_id)
    if not game:
        return f"Game {game_id} not found"

    result = game.reset()
    if result.success:
        return f"Environment reset: {result.new_state.model_dump()}"
    else:
        return f"Reset failed: {result.error}"


# CartPole-specific tools
@mcp.tool()
def cartpole_move_left(game_id: str, player: str) -> str:
    """Move CartPole cart left"""
    game = registry.get_game(game_id)
    if not game or game.type != "CartPole-v1":
        return f"CartPole game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 0}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Moved left: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


@mcp.tool()
def cartpole_move_right(game_id: str, player: str) -> str:
    """Move CartPole cart right"""
    game = registry.get_game(game_id)
    if not game or game.type != "CartPole-v1":
        return f"CartPole game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 1}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Moved right: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


# MountainCar-specific tools
@mcp.tool()
def mountain_car_push_left(game_id: str, player: str) -> str:
    """Push MountainCar left"""
    game = registry.get_game(game_id)
    if not game or game.type != "MountainCar-v0":
        return f"MountainCar game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 0}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Pushed left: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


@mcp.tool()
def mountain_car_no_push(game_id: str, player: str) -> str:
    """Don't push MountainCar"""
    game = registry.get_game(game_id)
    if not game or game.type != "MountainCar-v0":
        return f"MountainCar game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 1}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"No push: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


@mcp.tool()
def mountain_car_push_right(game_id: str, player: str) -> str:
    """Push MountainCar right"""
    game = registry.get_game(game_id)
    if not game or game.type != "MountainCar-v0":
        return f"MountainCar game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 2}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Pushed right: {result.new_state.model_dump()}"
    else:
        return f"Move failed: {result.error}"


# Breakout-specific tools
@mcp.tool()
def breakout_noop(game_id: str, player: str) -> str:
    """Do nothing in Breakout"""
    game = registry.get_game(game_id)
    if not game or game.type != "ALE/Breakout-v5":
        return f"Breakout game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 0}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"No-op: {result.new_state.model_dump()}"
    else:
        return f"Action failed: {result.error}"


@mcp.tool()
def breakout_fire(game_id: str, player: str) -> str:
    """Fire ball in Breakout"""
    game = registry.get_game(game_id)
    if not game or game.type != "ALE/Breakout-v5":
        return f"Breakout game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 1}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Fired: {result.new_state.model_dump()}"
    else:
        return f"Action failed: {result.error}"


@mcp.tool()
def breakout_right(game_id: str, player: str) -> str:
    """Move paddle right in Breakout"""
    game = registry.get_game(game_id)
    if not game or game.type != "ALE/Breakout-v5":
        return f"Breakout game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 2}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Moved right: {result.new_state.model_dump()}"
    else:
        return f"Action failed: {result.error}"


@mcp.tool()
def breakout_left(game_id: str, player: str) -> str:
    """Move paddle left in Breakout"""
    game = registry.get_game(game_id)
    if not game or game.type != "ALE/Breakout-v5":
        return f"Breakout game {game_id} not found"

    action_obj = GameAction(type="gym_step", payload={"action": 3}, player=player)
    result = game.make_move(action_obj)

    if result.success:
        return f"Moved left: {result.new_state.model_dump()}"
    else:
        return f"Action failed: {result.error}"


async def main():
    """Main entry point - async to match Dedalus pattern"""
    # Run the FastMCP server synchronously (FastMCP handles its own event loop)
    def run_server():
        mcp.run(transport='stdio')

    # Run in a thread to maintain async interface
    await asyncio.to_thread(run_server)


if __name__ == "__main__":
    asyncio.run(main())