import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Row, Col, Alert, Button, Modal } from "react-bootstrap";
import { AiOutlineLoading } from "react-icons/ai"; // Importing a loading icon

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [show, setShow] = useState(false);
  const [showViewReportButton, setShowViewReportButton] = useState(false);
  const [remainingTime, setRemainingTime] = useState(100); // Set your estimated time in seconds here
  const [timerInterval, setTimerInterval] = useState(null); // Timer interval ID

  const {
    application,
    environment,
    testCases,
    generateScreenshots,
    generateExcel,
  } = location.state || {};

  const user = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    const triggerRobotFramework = async () => {
      try {
        setLoading(true); // Show spinner during test execution
        setShow(true);
        setRemainingTime(150); // Reset remaining time

        // Start timer for countdown
        const intervalId = setInterval(() => {
          setRemainingTime((prevTime) => {
            if (prevTime <= 1) {
              clearInterval(intervalId); // Clear the interval
              return 0;
            }
            return prevTime - 1;
          });
        }, 1000);

        setTimerInterval(intervalId);

        const payload = {
          env: environment,
          user_id: user.id,
          testCases,
        };

        const response = await fetch(
          "http://localhost:9996/api/robo/trigger-robot",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to execute Robot Framework");
        }

        const data = await response.json();
        console.log(data.message);

        // If successful, show "View Report" button and stop spinner
        setShowViewReportButton(true);
        setLoading(false);
        setShow(false);
      } catch (err) {
        setLoading(false);
        setShow(false);
        setError(err.message);
      } finally {
        // Clear interval if still running
        if (timerInterval) {
          clearInterval(timerInterval);
        }
      }
    };

    triggerRobotFramework();
  }, [user.id, testCases, environment]);

  return (
    <Container>
      {/* Custom CSS */}
      <style>
        {`
          .icon-spin {
            animation: spin 1s infinite linear;
          }

          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }

          .error-alert {
            background-color: #eb1700; /* Use the specified color for error alert */
            color: white; /* Make text white for contrast */
          }

          .report-button {
            background-color: #eb1700; /* Button background color */
            border: none; /* Remove border */
          }

          .report-button:hover {
            background-color: #c81000; /* Darker shade on hover */
          }

          .modal-title {
            color: #eb1700; /* Title color in the modal */
          }
        `}
      </style>

      <Row className="justify-content-md-center mt-5">
        <Col md={6}>
          {error ? (
            <Alert variant="danger" className="error-alert">
              {error}
            </Alert>
          ) : (
            <div className="text-center">
              {showViewReportButton && (
                <Button
                  onClick={() =>
                    navigate("/report-viewer", {
                      state: {
                        application,
                        environment,
                        testCases,
                        generateScreenshots,
                        generateExcel,
                      },
                    })
                  }
                  variant="danger"
                  className="report-button"
                >
                  View Report
                </Button>
              )}
            </div>
          )}
        </Col>
      </Row>

      <Modal
        style={{ background: "rgba(0, 0, 0, 0.5)" }} // Semi-transparent background
        show={show}
        onHide={() => {}} // Disable close button
        backdrop="static" // Prevent closing when clicking outside
        keyboard={false} // Disable closing with keyboard (e.g., Esc key)
        centered // Centers the modal on the screen
      >
        <Modal.Header>
          <Modal.Title className="modal-title">Executing Tests</Modal.Title>
          {/* Remove close button */}
        </Modal.Header>
        <Modal.Body>
          <div className="text-center">
            <p>
              <AiOutlineLoading
                className="mb-3 icon-spin"
                size={40}
                color="#007bff"
              />
              {/* Animated loading icon */}
            </p>
            <p>
              We are currently executing your tests. Please do not close this
              window.
            </p>
            {/* <p>Time Remaining: {remainingTime} seconds</p>{" "} */}
            {/* Display remaining time */}
          </div>
        </Modal.Body>
      </Modal>
    </Container>
  );
}

export default ResultsPage;
