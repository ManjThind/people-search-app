
import React, { useState } from "react";
import axios from "axios";

const SearchComponent = () => {
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setPdfUrl("");

    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?name=${name}`, {
        responseType: "blob",
      });

      const file = new Blob([response.data], { type: "application/pdf" });
      const fileURL = URL.createObjectURL(file);
      setPdfUrl(fileURL);
    } catch (error) {
      alert("Error fetching data");
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>People Search</h2>
      <input type="text" placeholder="Enter name..." value={name} onChange={(e) => setName(e.target.value)} />
      <button onClick={handleSearch} disabled={loading}>{loading ? "Searching..." : "Search & Download PDF"}</button>
      {pdfUrl && <a href={pdfUrl} download="search_report.pdf">Download Report</a>}
    </div>
  );
};

export default SearchComponent;
