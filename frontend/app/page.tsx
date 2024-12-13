import {
  FaChessBishop,
  FaChessKing,
  FaChessKnight,
  FaChessPawn,
  FaChessQueen,
  FaChessRook,
} from "react-icons/fa";

type ChessPiece =
  | "rockBlack"
  | "knightBlack"
  | "bishopBlack"
  | "queenBlack"
  | "kingBlack"
  | "pawnBlack"
  | "rockWhite"
  | "knightWhite"
  | "bishopWhite"
  | "queenWhite"
  | "kingWhite"
  | "pawnWhite"
  | null;

type ChessBoard = ChessPiece[][];

const renderPiece = (piece: ChessPiece, eaten: boolean) => {
  const sizeClass = eaten ? "text-4xl" : "text-7xl"; // Utilise une classe CSS différente pour les pièces mangées
  const colorClass = piece?.includes("Black") ? "text-gray-700" : "text-white"; // Couleur selon la pièce

  switch (piece) {
    case "rockBlack":
      return <FaChessRook className={`${colorClass} ${sizeClass}`} />;
    case "knightBlack":
      return <FaChessKnight className={`${colorClass} ${sizeClass}`} />;
    case "bishopBlack":
      return <FaChessBishop className={`${colorClass} ${sizeClass}`} />;
    case "queenBlack":
      return <FaChessQueen className={`${colorClass} ${sizeClass}`} />;
    case "kingBlack":
      return <FaChessKing className={`${colorClass} ${sizeClass}`} />;
    case "pawnBlack":
      return <FaChessPawn className={`${colorClass} ${sizeClass}`} />;
    case "rockWhite":
      return <FaChessRook className={`${colorClass} ${sizeClass}`} />;
    case "knightWhite":
      return <FaChessKnight className={`${colorClass} ${sizeClass}`} />;
    case "bishopWhite":
      return <FaChessBishop className={`${colorClass} ${sizeClass}`} />;
    case "queenWhite":
      return <FaChessQueen className={`${colorClass} ${sizeClass}`} />;
    case "kingWhite":
      return <FaChessKing className={`${colorClass} ${sizeClass}`} />;
    case "pawnWhite":
      return <FaChessPawn className={`${colorClass} ${sizeClass}`} />;
    default:
      return null;
  }
};

const INITIAL_BOARD: ChessBoard = [
  [
    "rockWhite",
    "knightWhite",
    "bishopWhite",
    "queenWhite",
    "kingWhite",
    "bishopWhite",
    "knightWhite",
    "rockWhite",
  ],
  [
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
    "pawnWhite",
  ],
  [
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
  ],
  [
    "rockBlack",
    "knightBlack",
    "bishopBlack",
    "queenBlack",
    "kingBlack",
    "bishopBlack",
    "knightBlack",
    "rockBlack",
  ],
];

function getCapturedPieces(finalBoard: ChessBoard): {
  whitesCaptured: ChessPiece[];
  blacksCaptured: ChessPiece[];
} {
  const initialWhitePieces = INITIAL_BOARD.flat().filter(
    (piece) => piece && piece.includes("White")
  );
  const initialBlackPieces = INITIAL_BOARD.flat().filter(
    (piece) => piece && piece.includes("Black")
  );

  const finalWhitePieces = finalBoard
    .flat()
    .filter((piece) => piece && piece.includes("White"));
  const finalBlackPieces = finalBoard
    .flat()
    .filter((piece) => piece && piece.includes("Black"));

  const whitesCaptured: ChessPiece[] = [];
  const blacksCaptured: ChessPiece[] = [];

  const finalWhitePiecesCopy = [...finalWhitePieces];
  for (const piece of initialWhitePieces) {
    const index = finalWhitePiecesCopy.indexOf(piece);
    if (index !== -1) {
      finalWhitePiecesCopy.splice(index, 1);
    } else {
      whitesCaptured.push(piece);
    }
  }

  const finalBlackPiecesCopy = [...finalBlackPieces];
  for (const piece of initialBlackPieces) {
    const index = finalBlackPiecesCopy.indexOf(piece);
    if (index !== -1) {
      finalBlackPiecesCopy.splice(index, 1);
    } else {
      blacksCaptured.push(piece);
    }
  }

  return {
    whitesCaptured,
    blacksCaptured,
  };
}

const initialBoard: ChessBoard = [
  [
    "rockWhite",
    "knightWhite",
    null,
    "queenWhite",
    "kingWhite",
    "bishopWhite",
    "knightWhite",
    "rockWhite",
  ],
  [null, null, null, null, null, null, null, "pawnWhite"],
  [null, null, null, "pawnBlack", null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [
    null,
    "pawnBlack",
    "pawnBlack",
    null,
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
    "pawnBlack",
  ],
  [
    null,
    "knightBlack",
    "bishopBlack",
    "queenBlack",
    "kingBlack",
    null,
    "knightBlack",
    "rockBlack",
  ],
];

export default function Home() {
  const { whitesCaptured, blacksCaptured } = getCapturedPieces(initialBoard);
  console.log(whitesCaptured);
  console.log(blacksCaptured);

  return (
    <div className="flex bg-gray-700 h-screen">
      <div
        className="flex flex-col items-center justify-center"
        style={{ width: "auto" }}
      >
        <div
          className="grid grid-cols-8 border-black m-4 mr-0"
          style={{ width: "100vh", height: "100vh" }}
        >
          {initialBoard.map((row, rowIndex) =>
            row.map((piece, colIndex) => {
              const isBlack = (rowIndex + colIndex) % 2 === 1;
              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className={`relative flex items-center justify-center ${
                    isBlack ? "bg-[#769656]" : "bg-[#eeeed2]"
                  }`}
                  style={{ width: "100%", height: "100%" }}
                >
                  <div className="absolute w-full h-full flex items-center justify-center">
                    {renderPiece(piece, false)}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-start rounded-lg p-2 m-4 bg-gray-100 text-2xl font-semibold font-sans space-y-2">
        {/* Section Joueur 1 */}
        <div className="flex flex-col bg-[#769656] text-gray-100 items-center justify-center w-full rounded-lg p-2">
          <label>White Player :</label>
          {/* Pièces mangées par Joueur 1 */}
          <div className="flex flex-wrap gap-2 mt-2">
            {blacksCaptured.map((piece, index) => renderPiece(piece, true))}
          </div>
        </div>

        {/* Section Joueur 2 */}
        <div className="flex flex-col text-gray-700 bg-[#769656] items-center justify-center w-full rounded-lg p-2">
          <label>Black Player :</label>
          {/* Pièces mangées par Joueur 2 */}
          <div className="flex flex-wrap gap-2 mt-2">
            {/* Exemple d'icônes des pièces */}
            {whitesCaptured.map((piece, index) => renderPiece(piece, true))}
          </div>
        </div>
      </div>
    </div>
  );
}
