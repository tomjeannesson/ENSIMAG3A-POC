"use client"
import axios from "axios";
import { useEffect, useState } from "react";
import {
  FaChessBishop,
  FaChessKing,
  FaChessKnight,
  FaChessPawn,
  FaChessQueen,
  FaChessRook,
} from "react-icons/fa";

type ChessPiece =
  | "r"
  | "n"
  | "b"
  | "q"
  | "k"
  | "p"
  | "R"
  | "N"
  | "B"
  | "Q"
  | "K"
  | "P"
  | null;

const renderPiece = (piece: ChessPiece) => {
  switch (piece) {
    case "r":
      return <FaChessRook className="text-gray-700 text-7xl" />;
    case "n":
      return <FaChessKnight className="text-gray-700 text-7xl" />;
    case "b":
      return <FaChessBishop className="text-gray-700 text-7xl" />;
    case "q":
      return <FaChessQueen className="text-gray-700 text-7xl" />;
    case "k":
      return <FaChessKing className="text-gray-700 text-7xl" />;
    case "p":
      return <FaChessPawn className="text-gray-700 text-7xl" />;
    case "R":
      return <FaChessRook className="text-white text-7xl" />;
    case "N":
      return <FaChessKnight className="text-white text-7xl" />;
    case "B":
      return <FaChessBishop className="text-white text-7xl" />;
    case "Q":
      return <FaChessQueen className="text-white text-7xl" />;
    case "K":
      return <FaChessKing className="text-white text-7xl" />;
    case "P":
      return <FaChessPawn className="text-white text-7xl" />;
    default:
      return null;
  }
};

export default function Home() {
  const [board, setBoard] = useState<ChessPiece[][]>([
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
  ])

  useEffect(()=>{
    const  fetchData =  async ()=>{
      setInterval(()=>{ 
        const res = axios.get("http://poc-thaj:8000/")
        console.log(res)
    }, 1000);
  }
  fetchData()
  },[])
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
          {board.map((row, rowIndex) =>
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
                    {renderPiece(piece)}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-start rounded-lg p-2 m-4 bg-white text-2xl font-semibold font-sans space-y-2">
        {/* Section Joueur 1 */}
        <div className="flex flex-col bg-gray-200 items-center justify-center w-full rounded-lg p-2">
          <label>Joueur 1 :</label>
          {/* Pièces mangées par Joueur 1 */}
          <div className="flex flex-wrap gap-2 mt-2">
            {/* Exemple d'icônes des pièces */}
            <FaChessPawn className="text-black" />
            <FaChessKnight className="text-black" />
          </div>
        </div>

        {/* Section Joueur 2 */}
        <div className="flex flex-col bg-gray-200 items-center justify-center w-full rounded-lg p-2">
          <label>Joueur 2 :</label>
          {/* Pièces mangées par Joueur 2 */}
          <div className="flex flex-wrap gap-2 mt-2">
            {/* Exemple d'icônes des pièces */}
            <FaChessPawn className="text-black" />
            <FaChessRook className="text-black" />
            <FaChessQueen className="text-black" />
          </div>
        </div>
      </div>
    </div>
  );
}
