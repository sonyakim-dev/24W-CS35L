import { useState } from "react";
import Square from "./Square";
import calculateWinner from "./utils/calculateWinner";
import findValidMove from "./utils/findValidMove";

export default function App() {
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);
  const [lastRemovedPosition, setLastRemovedPosition] = useState(null);
  const [message, setMessage] = useState(null);

  const handleClick = (i) => {
    const currPlayer = xIsNext ? "X" : "O";
    const count = squares.filter((square) => square === currPlayer).length;

    if (calculateWinner(squares)) {
      return;
    }
    if (count < 3 && squares[i]) {
      setMessage("* Invalid movement. Select again.");
      return;
    }
    // when count is 3, it's in a moving phase
    if (count == 3) {
      // time to remove
      if (lastRemovedPosition === null) {
        // if there is a center piece, must remove it
        if (squares[4] === currPlayer) {
          if (i !== 4) {
            setMessage("* Must select the center piece.");
            return;
          }
          setLastRemovedPosition(i);
          setMessage(null);
          return;
        }
        // when there is no center piece and the selected piece is the current player
        else if (squares[i] === currPlayer) {
          // check if it's movable
          const validMoves = findValidMove(squares, i);
          if (validMoves.length === 0) {
            setMessage("* Not able to remove this piece. Select again.");
            setLastRemovedPosition(null);
            return;
          }
          setLastRemovedPosition(i);
          setMessage(null);
          return;
        }
        setLastRemovedPosition(null);
        setMessage("* Invalid movement. Select again.");
      }
      // time to add
      else {
        const validMoves = findValidMove(squares, lastRemovedPosition);
        // if the selected square is a valid move, remove the piece and place it
        if (validMoves.includes(i)) {
          setSquares((prev) =>
            prev.map((square, index) => {
              if (lastRemovedPosition === index) return null;
              else if (index === i) return currPlayer;
              return square;
            })
          );
          setLastRemovedPosition(null);
          setXIsNext((prev) => !prev);
          setMessage(null);
          return;
        }
        setLastRemovedPosition(null);
        setMessage("* Invalid movement. Select again.");
      }
    }
    // place piece in empty square
    else {
      setSquares((prev) =>
        prev.map((square, index) => (index === i ? currPlayer : square))
      );
      setXIsNext((prev) => !prev);
      setMessage(null);
    }
  };

  const winner = calculateWinner(squares);
  const status = winner
    ? `Winner: ${winner}`
    : `Next player: ${xIsNext ? "X" : "O"}`;

  return (
    <div className="App">
      <div className="status">{status}</div>
      <div className="board-row">
        <Square
          index={0}
          value={squares[0]}
          onSquareClick={() => handleClick(0)}
          selected={lastRemovedPosition}
        />
        <Square
          index={1}
          value={squares[1]}
          onSquareClick={() => handleClick(1)}
          selected={lastRemovedPosition}
        />
        <Square
          index={2}
          value={squares[2]}
          onSquareClick={() => handleClick(2)}
          selected={lastRemovedPosition}
        />
      </div>
      <div className="board-row">
        <Square
          index={3}
          value={squares[3]}
          onSquareClick={() => handleClick(3)}
          selected={lastRemovedPosition}
        />
        <Square
          index={4}
          value={squares[4]}
          onSquareClick={() => handleClick(4)}
          selected={lastRemovedPosition}
        />
        <Square
          index={5}
          value={squares[5]}
          onSquareClick={() => handleClick(5)}
          selected={lastRemovedPosition}
        />
      </div>
      <div className="board-row">
        <Square
          index={6}
          value={squares[6]}
          onSquareClick={() => handleClick(6)}
          selected={lastRemovedPosition}
        />
        <Square
          index={7}
          value={squares[7]}
          onSquareClick={() => handleClick(7)}
          selected={lastRemovedPosition}
        />
        <Square
          index={8}
          value={squares[8]}
          onSquareClick={() => handleClick(8)}
          selected={lastRemovedPosition}
        />
      </div>
      <div className="message" style={{ color: "red", fontSize: 12 }}>
        {message ?? null}
      </div>
    </div>
  );
}
