import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Alert, Card } from "react-bootstrap";
import { FaDownload, FaUpload, FaExclamationTriangle } from "react-icons/fa";

function TestTemplatePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const {
    application,
    environment,
    testCases,
    generateScreenshots,
    generateExcel,
  } = location.state || {};

  const user = JSON.parse(localStorage.getItem("user"));

  const [selectedFiles, setSelectedFiles] = useState({});
  const [uploadMessages, setUploadMessages] = useState({});

  const handleDownload = (testCase) => {
    const filePath = `${process.env.PUBLIC_URL}/${testCase}.xlsx`;
    const link = document.createElement("a");
    link.href = filePath;
    link.download = `${testCase}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Handle file selection for a specific test case
  const handleFileChange = async (testCase, event) => {
    const file = event.target.files[0];
    if (
      file &&
      file.type !==
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ) {
      setUploadMessages((prev) => ({
        ...prev,
        [testCase]: "Only .xlsx files are allowed!",
      }));
    } else if (file) {
      setSelectedFiles((prev) => ({
        ...prev,
        [testCase]: file,
      }));
      setUploadMessages((prev) => ({
        ...prev,
        [testCase]: "",
      }));
    } else {
      // Clear everything if no file selected
      setSelectedFiles((prev) => ({
        ...prev,
        [testCase]: null,
      }));
      setUploadMessages((prev) => ({
        ...prev,
        [testCase]: "",
      }));
    }
  };

  // Handle file upload for a specific test case
  const handleUpload = async (testCase) => {
    const selectedFile = selectedFiles[testCase];
    if (!selectedFile) {
      setUploadMessages((prev) => ({
        ...prev,
        [testCase]: "Please select a file first!",
      }));
      return;
    }

    const apiUrl = `http://localhost:9996/api/upload/${environment}/${user.id}`;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadMessages((prev) => ({
          ...prev,
          [testCase]: "File uploaded successfully.",
        }));
        // Reset the selected file after successful upload
        setSelectedFiles((prev) => ({
          ...prev,
          [testCase]: null,
        }));
      } else {
        throw new Error("File upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadMessages((prev) => ({
        ...prev,
        [testCase]: "Error uploading file: " + error.message,
      }));
    }
  };

  const canProceed = testCases?.every(
    (testCase) =>
      uploadMessages[testCase] &&
      uploadMessages[testCase].includes("successfully")
  );

  const handleSubmit = (e) => {
    e.preventDefault();

    if (canProceed) {
      navigate("/results", {
        state: {
          application,
          environment,
          testCases,
          generateScreenshots,
          generateExcel,
        },
      });
    } else {
      alert("Please upload all files successfully before proceeding.");
    }
  };

  const getSpecialSections = (headers) => {
    if (!headers) return { rescind: [], correction: [] };
    
    const rescind = headers.filter(h => 
      h.header.toLowerCase().includes('rescind')
    );
    const correction = headers.filter(h => 
      h.header.toLowerCase().includes('correction')
    );
    
    return { rescind, correction };
  };

  return (
    <Container className="mb-5">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2
          style={{
            textAlign: "left",
            display: "block",
            color: "#eb1700",
          }}
          className="py-3"
        >
          Test Template
        </h2>
        <button
          onClick={() => navigate(-1)}
          className="btn"
          style={{
            backgroundColor: "#eb1700",
            color: "white",
            border: "none",
            padding: "8px 16px",
          }}
        >
          ← Back to Selections
        </button>
      </div>

      {generateScreenshots && (
        <Alert variant="info" className="mb-3">
          📸 Screenshots will be generated for errors.
        </Alert>
      )}
      {generateExcel && (
        <Alert variant="info" className="mb-3">
          📊 An Excel report will be generated for the test results.
        </Alert>
      )}

      {/* General Instructions Card */}
      <Card className="mb-4" style={{ border: "1px solid #3498db", borderRadius: "8px" }}>
        <Card.Header style={{ backgroundColor: "#e8f4fd", borderBottom: "1px solid #3498db" }}>
          <h5 className="mb-0" style={{ color: "#2c3e50" }}>
            📋 General Instructions
          </h5>
        </Card.Header>
        <Card.Body>
          <Alert variant="warning" className="mb-3">
            <FaExclamationTriangle className="me-2" />
            <strong>Important: Review All Template Sections</strong>
            <br />
            Please check all headers in row #1 of the downloaded template for all the subprocesses that can be tested.
          </Alert>
          
          <Alert variant="danger" className="mb-0">
            <strong>⚠️ Special Testing Sections</strong>
            <br />
            If you want to test <strong>Rescind</strong> and <strong>Correction</strong> processes, 
            please scroll to the end of the spreadsheet to find the respective columns.
          </Alert>
        </Card.Body>
      </Card>

      {testCases &&
        testCases.map((testCase) => (
          <Card key={testCase} className="mb-4" style={{ border: "1px solid #ddd", borderRadius: "8px" }}>
            <Card.Header style={{ backgroundColor: "#f8f9fa", borderBottom: "1px solid #ddd" }}>
              <h4 className="mb-2" style={{ color: "#2c3e50" }}>
                {testCase.replaceAll("_", " ")}
              </h4>
              <p className="mb-0 text-muted">
                Note: To proceed download the template and upload it with test data along with country selection.
              </p>
            </Card.Header>
            
            <Card.Body>
              {/* Action Buttons */}
              <div className="d-flex align-items-center mb-3">
                <button
                  onClick={() => handleDownload(testCase)}
                  className="btn btn-outline-success btn-sm me-3"
                  style={{
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <FaDownload className="me-2" />
                  Download
                </button>
                
                <button
                  onClick={() => handleUpload(testCase)}
                  className="btn btn-outline-primary btn-sm me-3"
                  style={{
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <FaUpload className="me-2" />
                  Upload
                </button>
                
                <input
                  type="file"
                  accept=".xlsx"
                  onChange={(event) => handleFileChange(testCase, event)}
                  id={`file-upload-${testCase}`}
                  className="form-control"
                  style={{ width: "300px" }}
                />
              </div>

              {/* Upload Status */}
              {uploadMessages[testCase] && (
                <Alert
                  variant={
                    uploadMessages[testCase].includes("successfully")
                      ? "success"
                      : "danger"
                  }
                  className="mb-3"
                >
                  {uploadMessages[testCase]}
                </Alert>
              )}


            </Card.Body>
          </Card>
        ))}



      {canProceed && (
        <div className="text-center">
          <button
            onClick={handleSubmit}
            style={{
              backgroundColor: "#eb1700",
              color: "white",
              border: "none",
              padding: "12px 30px",
              fontSize: "16px",
              fontWeight: "bold",
              borderRadius: "4px",
              cursor: "pointer"
            }}
          >
            Proceed to Results
          </button>
        </div>
      )}
    </Container>
  );
}

export default TestTemplatePage;