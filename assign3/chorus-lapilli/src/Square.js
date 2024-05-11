const Square = ({ index, value, onSquareClick, selected }) => {
  const className = index === selected ? "square selected" : "square";
  return (
    <button className={className} onClick={onSquareClick}>
      {value}
    </button>
  );
};

export default Square;
