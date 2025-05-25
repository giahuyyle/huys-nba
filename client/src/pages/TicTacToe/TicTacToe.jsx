import { useState, useEffect } from "react";
import api from "../../utils/api";
import { teamNicknames } from "../../utils/Teams";
import "./TicTacToe.css";

const teamKeys = Object.keys(teamNicknames);

function capitalize(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
};

function getRandomTeams(n) {
    const arr = [...teamKeys];
    const result = [];
    while (result.length < n && arr.length > 0) {
        const idx = Math.floor(Math.random() * arr.length);
        result.push(arr.splice(idx, 1)[0]);
    }
    return result;
}

const BOARD_SIZE = 4;

const TicTacToe = () => {
    const [input, setInput] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [selectedTeams, setSelectedTeams] = useState([]);
    const [selectedCell, setSelectedCell] = useState(null); // {row, col}
    const [board, setBoard] = useState(
        Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null))
    );
    const [helper, setHelper] = useState("Select a cell to start");
    const [commonPlayers, setCommonPlayers] = useState({});
    const [lastCheckedPlayer, setLastCheckedPlayer] = useState(null);
    const [lastCheckResult, setLastCheckResult] = useState(null);

    useEffect(() => {
        setSelectedTeams(getRandomTeams(6));
    }, []);

    useEffect(() => {
        const fetchCommonPlayers = async () => {
            if (selectedTeams.length !== 6) return;
            try {
                const rows = selectedTeams.slice(0, 3).join(",");
                const cols = selectedTeams.slice(3, 6).join(",");
                const response = await api.get(`/common_players?rows=${rows}&cols=${cols}`);
                setCommonPlayers(response.data || {});
            } catch (err) {
                console.error("Error fetching common players:", err);
                setCommonPlayers({});
            }
        };
        fetchCommonPlayers();
    }, [selectedTeams]);

    useEffect(() => {
        if (!selectedCell) {
            setHelper("Select a cell");
        } else {
            // Only for non-header cells
            if (selectedCell.row > 0 && selectedCell.col > 0) {
                const team1 = capitalize(selectedTeams[selectedCell.col - 1]);
                const team2 = capitalize(selectedTeams[selectedCell.row + 2]);
                setHelper(`Currently selecting cell between ${capitalize(team1)} and ${capitalize(team2)}`);
            }
        }
    }, [selectedCell, selectedTeams]);

    useEffect(() => {
        const fetchPlayers = async () => {
            if (input.trim() === "" || input.length < 3) {
                setSuggestions([]);
                return;
            }
            try {
                const response = await api.get(`/players/${encodeURIComponent(input)}`);
                setSuggestions(response.data || []);
            } catch (err) {
                setSuggestions([]);
            }
        };
        const timeout = setTimeout(fetchPlayers, 300);
        return () => clearTimeout(timeout);
    }, [input]);

    const validatePlayer = (player, team1, team2, row, col) => {
        if (!player || !commonPlayers) return false;
        // only validate cells not in 1st row/column
        if (row <= 0 || col <= 0) return false;
        const rowTeam = selectedTeams[row + 2];
        const colTeam = selectedTeams[col - 1];
        const key = `('${colTeam}', '${rowTeam}')`;
        const validPlayers = commonPlayers[key] || [];
        return validPlayers.includes(player.additionals);
    };

    const handleSuggestionClick = (player) => {
        if (!selectedCell) return;
        const { row, col } = selectedCell;
        const team1 = selectedTeams[selectedCell.col - 1];
        const team2 = selectedTeams[selectedCell.row + 2];
        const isValid = validatePlayer(player, team1, team2, row, col);

        setLastCheckedPlayer(player);
        setLastCheckResult(isValid);

        if (isValid) {
            const newBoard = board.map(arr => arr.slice());
            newBoard[row][col] = player.name;
            setBoard(newBoard);
            setHelper(`${player.name} has been selected`);
            setSelectedCell(null);
            setInput("");
            setSuggestions([]);
        } else {
            setHelper(`${player.name} has not played for both ${capitalize(team1)} and ${capitalize(team2)}`);
        }
    };

    const renderCell = (row, col) => {
        if (row === 0 && col === 0) return <img src="src/assets/logo.png" />;
        if (row === 0 && col > 0) {
            const TeamLogo = teamNicknames[selectedTeams[col - 1]];
            return TeamLogo ? <TeamLogo /> : null;
        }
        if (col === 0 && row > 0) {
            const TeamLogo = teamNicknames[selectedTeams[row + 2]];
            return TeamLogo ? <TeamLogo /> : null;
        }
        // Player name if filled
        if (board[row][col]) return board[row][col];
        // Highlight if selected
        if (selectedCell && selectedCell.row === row && selectedCell.col === col) {
            return <span className="selected-cell">?</span>;
        }
        return null;
    };

    return (
        <div className="tic-tac-toe">
            <div className="helper">
                <h2>{helper}</h2>
            </div>
            <div className="board">
                {Array.from({ length: BOARD_SIZE * BOARD_SIZE }).map((_, idx) => {
                    const row = Math.floor(idx / BOARD_SIZE);
                    const col = idx % BOARD_SIZE;
                    return (
                        <div
                            key={idx}
                            className={`cell${selectedCell && selectedCell.row === row && selectedCell.col === col ? " active" : ""}`}
                            onClick={() => {
                                // Only allow selection for non-header cells
                                if (row === 0 || col === 0) return;
                                if (board[row][col]) return;
                                setSelectedCell({ row, col });
                            }}
                        >
                            {selectedTeams.length === 6 ? renderCell(row, col) : null}
                        </div>
                    );
                })}
            </div>
            <div className="player-field">
                <input
                    type="text"
                    placeholder="Select a Player"
                    className="player-input"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    autoComplete="off"
                    disabled={!selectedCell}
                />
                <button className="give-up-button">Give Up?</button>
                {suggestions.length > 0 && selectedCell && (
                    <ul className="suggestions-list">
                        {suggestions.map((player) => (
                            <li key={player.id} onClick={() => handleSuggestionClick(player)}>
                                {player.name}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default TicTacToe;