import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
    const [cpes, setCpes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(15);
    const [total, setTotal] = useState(0);
    const [popoverId, setPopoverId] = useState(null);

    const [titleFilter, setTitleFilter] = useState('');
    const [uri22Filter, setUri22Filter] = useState('');
    const [uri23Filter, setUri23Filter] = useState('');
    const [dateFilter, setDateFilter] = useState('');

    useEffect(() => {
        const getData = async () => {
            setLoading(true);
            try {
                const isSearching = titleFilter || uri22Filter || uri23Filter || dateFilter;
                let url = `http://localhost:8000/api/cpes?page=${page}&limit=${limit}`;
                
                if (isSearching) {
                    url = `http://localhost:8000/api/cpes/search?cpe_title=${titleFilter}&cpe_22_uri=${uri22Filter}&cpe_23_uri=${uri23Filter}&deprecation_date=${dateFilter}`;
                }

                const res = await axios.get(url);
                
                if (isSearching) {
                    setCpes(res.data.data);
                    setTotal(res.data.data.length); 
                } else {
                    setCpes(res.data.data);
                    setTotal(res.data.total);
                }
            } catch (err) {
                console.error("Error fetching data:", err);
            }
            setLoading(false);
        };

        const delayDebounceFn = setTimeout(() => {
            getData();
        }, 500);

        return () => clearTimeout(delayDebounceFn);
    }, [page, limit, titleFilter, uri22Filter, uri23Filter, dateFilter]);

    const formatDate = (dateString) => {
        if (!dateString) return "N/A";
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>CPE Dictionary API Explorer</h1>

            <div className="search-container">
                <input type="text" placeholder="Search Title" value={titleFilter} onChange={e => setTitleFilter(e.target.value)} />
                <input type="text" placeholder="Search CPE 2.2" value={uri22Filter} onChange={e => setUri22Filter(e.target.value)} />
                <input type="text" placeholder="Search CPE 2.3" value={uri23Filter} onChange={e => setUri23Filter(e.target.value)} />
                <input type="date" value={dateFilter} onChange={e => setDateFilter(e.target.value)} />
                
                <select value={limit} onChange={e => setLimit(e.target.value)}>
                    <option value="15">15 per page</option>
                    <option value="25">25 per page</option>
                    <option value="50">50 per page</option>
                </select>
            </div>

            {loading ? <p>Loading data...</p> : (
                <>
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>CPE 2.2 URI</th>
                                <th>CPE 2.3 URI</th>
                                <th>Dep-Date 22</th>
                                <th>Dep-Date 23</th>
                                <th>References</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cpes.map(item => (
                                <tr key={item.id}>
                                    <td><div className="truncate-text" title={item.cpe_title}>{item.cpe_title}</div></td>
                                    <td>{item.cpe_22_uri}</td>
                                    <td>{item.cpe_23_uri}</td>
                                    <td>{formatDate(item.cpe_22_deprecation_date)}</td>
                                    <td>{formatDate(item.cpe_23_deprecation_date)}</td>
                                    <td style={{ position: 'relative' }}>
                                        {item.reference_links.slice(0, 2).map((link, i) => (
                                            <div key={i}><a href={link} target="_blank" className="truncate-text">{link}</a></div>
                                        ))}
                                        {item.reference_links.length > 2 && (
                                            <button onClick={() => setPopoverId(popoverId === item.id ? null : item.id)} style={{ padding: '2px 5px', fontSize: '10px' }}>
                                                {item.reference_links.length - 2} more
                                            </button>
                                        )}
                                        {popoverId === item.id && (
                                            <div className="popover-basic">
                                                {item.reference_links.map((link, i) => (
                                                     <div key={i}><a href={link} target="_blank">{link}</a></div>
                                                ))}
                                                <button onClick={() => setPopoverId(null)}>Close</button>
                                            </div>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <div className="pagination">
                        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</button>
                        <span>Page {page}</span>
                        <button disabled={cpes.length < limit} onClick={() => setPage(page + 1)}>Next</button>
                    </div>
                </>
            )}
        </div>
    );
};

export default App;
