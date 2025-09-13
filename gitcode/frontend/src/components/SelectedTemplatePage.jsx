import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";
import { FaDownload, FaUpload } from "react-icons/fa";

function SelectedTemplatePage() {
  const location = useLocation();
  const navigate = useNavigate();
  // Extract data passed from the SelectionsPage
  const {
    application,
    environment,
    testCases,
    generateScreenshots,
    generateExcel,
  } = location.state || {};

  const handleBack = () => {
    navigate("/selections"); // Navigate back to the selection page
  };

  const passTestName = (testName) => {
    navigate("/TestTemplate", { state: testName });
  };
  const handleSubmit = (e) => {
    e.preventDefault();

    navigate("/results", {
      state: {
        application,
        environment,
        testCases,
        generateScreenshots,
        generateExcel,
      },
    });
  };

  const env = localStorage.getItem("enviroment");
  const user = JSON.parse(localStorage.getItem("user"));

  const filePath = process.env.PUBLIC_URL + `/${location.state}.xlsx`;

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = filePath;
    link.download = `${location.state}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadMessage(""); // Clear previous messages
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadMessage("Please select a file to upload");
      setMessageType("error");
      return;
    }

    const apiUrl = `http://localhost:9996/api/upload/${env}/${user.id}`;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const jsonResponse = await response.json();
        setUploadMessage("File uploaded successfully ");
        setMessageType("success");
        setSelectedFile(null); // Reset the selected file after successful upload
      } else {
        setUploadMessage("File upload failed: " + response.statusText);
        setMessageType("error");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadMessage("Error uploading file: " + error.message);
      setMessageType("error");
    }
  };

  const messageStyle = {
    color: messageType === "success" ? "green" : "red",
    marginLeft: "10px",
  };

  return (
    <Container>
      <Row className="justify-content-md-center mt-5">
        <Col md={6}>
          <form onSubmit={handleSubmit}>
            <div className="d-flex justify-content-between align-items-center mb-4">
              {/* <h2>Auto-Test-App</h2> */}
              <Button variant="primary" size="sm" onClick={handleBack}>
                Back
              </Button>
            </div>

            <div>
              <h4>Tests Case Templates Selected</h4>
              <p>Note: Download the template and upload it with test data.</p>

              <div className="mb-3">
                <ol>
                  {testCases &&
                    testCases.map((test, index) => (
                      <>
                        <br></br>
                        <span>{test}</span>
                        <div className="align-content-center d-flex">
                          <button
                            type="button"
                            onClick={handleDownload}
                            className="btn btn-outline-success btn-sm"
                            style={{ display: "flex", alignItems: "center" }}
                          >
                            <FaDownload style={{ marginRight: "5px" }} />
                            Download
                          </button>{" "}
                          &nbsp; &nbsp; &nbsp;
                          <button
                            onClick={handleUpload}
                            type="button"
                            className="btn btn-outline-primary btn-sm"
                            style={{
                              display: "flex",
                              alignItems: "center",
                              marginLeft: "10px",
                            }}
                          >
                            <FaUpload style={{ marginRight: "5px" }} />
                            Upload
                          </button>
                          &nbsp; &nbsp; &nbsp;
                          <input
                            style={{ width: "300px" }}
                            onChange={handleFileChange}
                            type="file"
                            id="formFile"
                          />
                          {uploadMessage && (
                            <span style={messageStyle}>{uploadMessage}</span>
                          )}
                        </div>
                      </>
                    ))}
                </ol>
              </div>
            </div>
            <Button variant="primary" type="submit" className="w-100 mb-3">
              Proceed
            </Button>
          </form>
        </Col>
      </Row>
    </Container>
  );
}

export default SelectedTemplatePage;
