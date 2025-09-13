import { useLocation, useNavigate } from "react-router-dom";

function IntegrationTestResults() {
  const location = useLocation();
  const navigate = useNavigate();

  const testCaseSelected = location.state;

  const handleClose = () => {
    navigate(-1);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2>{testCaseSelected}</h2> {/* This is  Hardcoded Template Name */}
        <button
          onClick={handleClose}
          style={{
            backgroundColor: "red",
            color: "white",
            border: "none",
            padding: "5px 10px",
            cursor: "pointer",
          }}
        >
          X
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Test Result</h3>
        <p>
          <strong>Status</strong>: Pass
        </p>
        <p>
          <strong>Error Messages</strong>: None
        </p>
        <p>
          <strong>Logs</strong>: [Log information will display here]
        </p>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Integration Test Results</h3>
        <p>
          <strong>Pass Rate</strong>: 66.67%
        </p>
        <p>
          <strong>Fail Rate</strong>: 33.33%
        </p>
      </div>

      <table
        style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px" }}
      >
        <thead>
          <tr>
            <th
              style={{
                border: "1px solid #ddd",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Test Case ID
            </th>
            <th
              style={{
                border: "1px solid #ddd",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Test Name
            </th>
            <th
              style={{
                border: "1px solid #ddd",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Execution Time
            </th>
            <th
              style={{
                border: "1px solid #ddd",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Result
            </th>
            <th
              style={{
                border: "1px solid #ddd",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Comments
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>TC001</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              Verify login functionality
            </td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>2 min</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>Pass</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              All checks passed successfully
            </td>
          </tr>
          <tr>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>TC002</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              Verify User Role
            </td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>1 min</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>Pass</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              All checks passed successfully
            </td>
          </tr>
          <tr>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>TC003</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              Verify User Details
            </td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>3 min</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>Fail</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>
              All checks passed successfully
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default IntegrationTestResults;
