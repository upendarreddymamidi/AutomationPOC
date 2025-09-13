import React, { useEffect, useState } from "react";
// import MultiSelectDropdown from "./MultiSelectDropdown.jsx";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

function SelectionsPage() {
  const navigate = useNavigate();
  const [applications, setApplications] = useState([]);
  const [environments, setEnvironments] = useState([]);
  const [testCasesOptions, setTestCasesOptions] = useState([]);

  const [application, setApplication] = useState("");
  const [environment, setEnvironment] = useState("");
  const [testCases, setTestCases] = useState(""); // Change type to string for single selection
  // const [generateScreenshots, setGenerateScreenshots] = useState(false);
  // const [generateExcel, setGenerateExcel] = useState(false);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("authToken");

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await fetch(
          "http://localhost:9996/api/selections/get/data",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "Failed to fetch applications");
        }

        const data = await response.json();
        setApplications(data.data.applications || []);
        setEnvironments(data.data.environment || []);
        setTestCasesOptions(data.data.testCases || []);

        // Set default values if available
        setApplication(data.data.applications?.[0] || "");
        setEnvironment(data.data.environment?.[0] || "");
        setTestCases(data.data.testCases?.[0] || ""); // Set the first option as default
      } catch (err) {
        setError(
          err.message || "An error occurred while fetching applications."
        );
      }
    };
    fetchApplications();
  }, [token]);

  const handleApplicationChange = (event) => {
    setApplication(event.target.value);
  };

  const handleEnvironmentChange = (event) => {
    setEnvironment(event.target.value);
  };

  const handleTestCasesChange = (event) => {
    setTestCases(event.target.value); // Update to a single value
  };

  // const handleScreenshotsChange = (event) => {
  //   setGenerateScreenshots(event.target.checked);
  // };

  // const handleExcelChange = (event) => {
  //   setGenerateExcel(event.target.checked);
  // };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    const payload = {
      application,
      environment,
      testCases: [testCases], // Wrap in an array
      // generateScreenshots,
      // generateExcel,
    };

    try {
      const response = await fetch("http://localhost:9996/api/selections", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to submit selections");
      } else {
        const data = await response.json();
        localStorage.setItem("environment", data.data.environment);

        navigate("/TestTemplate", {
          state: {
            application,
            environment,
            testCases: [testCases], // Wrap in an array for navigation
            // generateScreenshots,
            // generateExcel,
          },
        });
      }
    } catch (err) {
      setError(
        err.message || "An error occurred while submitting the selections."
      );
    } finally {
      setLoading(false);
    }
  };

  const buttonStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  return (
    <Container>
      <Row className="justify-content-md-center mt-5">
        <Col md={6}>
          <div className="d-flex justify-content-center align-items-center mb-4">
            <h2
              style={{
                textAlign: "left",
                display: "block",
                marginLeft: "-70px",
                color: "#eb1700",
              }}
            >
              Test Data Automation Tool
            </h2>
            <a
              style={buttonStyle}
              href="/login"
              className=" ms-5 btn btn-primary btn-sm"
            >
              Back to Login
            </a>
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="application" className="m-3">
              <Form.Label>Select the Application to Test:</Form.Label>
              <select
                onChange={handleApplicationChange}
                className="form-select"
                aria-label="Select Application"
                value={application}
              >
                {applications.map((app) => (
                  <option key={app} value={app}>
                    {app}
                  </option>
                ))}
              </select>
            </Form.Group>
            <Form.Group controlId="environment" className="m-3">
              <Form.Label>Select the Environment:</Form.Label>
              <select
                onChange={handleEnvironmentChange}
                className="form-select"
                aria-label="Select Environment"
                value={environment}
              >
                {environments.map((env) => (
                  <option key={env} value={env}>
                    {env}
                  </option>
                ))}
              </select>
            </Form.Group>
            <Form.Group controlId="testCases" className="m-3">
              <Form.Label>Select the Business Process:</Form.Label>
              <select
                onChange={handleTestCasesChange}
                className="form-select"
                aria-label="Select Test Cases"
                value={testCases} // Ensuring selected value is displayed correctly
              >
                {testCasesOptions.map((testCaseOption) => (
                  <option key={testCaseOption} value={testCaseOption}>
                    {testCaseOption.replaceAll("_", " ")}
                  </option>
                ))}
              </select>
            </Form.Group>
            {/* <Form.Group controlId="screenshots" className="m-3">
              <Form.Check
                type="checkbox"
                label="Generate Error Screenshots for Test case results"
                checked={generateScreenshots}
                onChange={handleScreenshotsChange}
              />
            </Form.Group>
            <Form.Group controlId="excel" className="m-3">
              <Form.Check
                type="checkbox"
                label="Generate Test Case Results to an Excel File"
                checked={generateExcel}
                onChange={handleExcelChange}
              />
            </Form.Group> */}
            <p>Note: Country selection must be made in the template after downloading in next screen</p>
            {error && <p className="m-3 text-danger">{error}</p>}
            <div className="d-flex justify-content-center">
              <Button
                variant="primary"
                type="submit"
                size="lg"
                disabled={loading}
                style={buttonStyle}
              >
                {loading ? "Submitting.." : "Proceed"}
              </Button>
            </div>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default SelectionsPage;
