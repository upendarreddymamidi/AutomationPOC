function ReportViewer() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Test Report</h2>
      <p>
        <a
          href={`http://localhost:9996/api/robo/download-report/${user.id}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Report
        </a>{" "}
        <a
          href={`http://localhost:9996/api/robo/download-zip/${user.id}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Screenshots
        </a>
      </p>
    </div>
  );
}

export default ReportViewer;
