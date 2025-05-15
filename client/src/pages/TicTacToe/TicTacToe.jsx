import { useState, useEffect } from "react";
import api from "../../api";
import teams from "./Teams";
import "./TicTacToe.css";

const teamKeys = Object.keys(teams);

function getRandomTeams(n) {
    const arr = [...teamKeys];
    const result = [];

    while (result.length < n && arr.length > 0) {
        const i = Math.floor(Math.random() * arr.length);
        // pop the team at index i from the array, and append it to result
        result.push(arr.splice(i, 1)[0]);
    }
    return result;
};

const TicTacToe = () => {
    const [input, setInput] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [selectedTeams, setSelectedTeams] = useState([]);

    useEffect(() => {
        setSelectedTeams(getRandomTeams(6));
    }, []);

    useEffect (() => {
        const fetchPlayers = async () => {
            if (input.trim() === "" || input.length < 3) {
                setSuggestions([]);
                return;
            }
            try {
                const response = await api.get(`/players/${encodeURIComponent(input)}`);
                setSuggestions(response.data || []);
                console.log(suggestions);
            } catch (err) {
                setSuggestions([]);
                console.error("Error fetching players:", err);
            }
        }

        // only fetch players after user stops typing for 300ms (0.3s)
        const timeout = setTimeout(fetchPlayers, 300);
        return () => clearTimeout(timeout);
    }, [input]);

    const renderCell = (row, col) => {
        // Top-left cell is empty
        if (row === 0 && col === 0) return null;
        // First row (excluding top-left): teams 0,1,2
        else if (row === 0 && col > 0) {
            const Logo = teams[selectedTeams[col - 1]]
            return <Logo />;
        }
        // First column (excluding top-left): teams 3,4,5
        else if (col === 0 && row > 0) {
            const Logo = teams[selectedTeams[row + 2]];
            return <Logo />;
        }
        // Other cells: empty
        return null;
    };

    return (
        <div className="tic-tac-toe">
            <div className="board">
                {Array.from({ length: 16 }).map((_, idx) => {
                    const row = Math.floor(idx / 4);
                    const col = idx % 4;
                    return (
                        <div key={idx} className="cell">
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
                />
                <button className="give-up-button">Give Up?</button>
                { suggestions.length > 0 && (
                    <ul className="suggestions-list">
                        {
                            suggestions.map((player) => (
                                <li key={player.id}>{player.name}</li>
                            ))
                        }
                    </ul>
                )}
            </div>
        </div>
    );
};

export default TicTacToe;