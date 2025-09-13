import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

function ResetPasswordAdmin() {
  const navigate = useNavigate();
  const location = useLocation();
  const [useremailid, setUserEmailId] = useState(
    location.state?.userEmailId || ""
  ); // Fetch email from location state
  const [NewPassword, setNewPassword] = useState("");
  const [ConfirmPassword, setConfirmPassword] = useState("");
  const [showNewPassword, setNewShowPassword] = useState(false);
  const [showConfirmPassword, setConfirmShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState("");

  const buttonHoverStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "useremailid") setUserEmailId(value);
    if (name === "NewPassword") setNewPassword(value);
    if (name === "ConfirmPassword") setConfirmPassword(value);

    if (errors) setErrors("");
    if (message) setMessage("");
  };

  const toggleNewPasswordVisibility = () => {
    setNewShowPassword(!showNewPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setConfirmShowPassword(!showConfirmPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!useremailid || !NewPassword || !ConfirmPassword) {
      setErrors("Email and Password are required.");
      return;
    }

    if (NewPassword !== ConfirmPassword) {
      setErrors("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:9996/api/users/updatepwd",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: useremailid,
            newPassword: NewPassword,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setErrors("");
        setMessage(data.message);
        // Redirect to login page after resetting password
        navigate("/admin/dashboard");
      } else {
        setErrors(data.error);
      }
    } catch (error) {
      setErrors("Failed to reset password. Please try again later.");
    }
  };

  return (
    <Container className="container-fluid align-items-center">
      <Row className="justify-content-md-center mt-5">
        <Col xs={12} md={6}>
          <h2
            style={{
              textAlign: "left",
              display: "block",

              color: "#eb1700",
            }}
            className="text-center mb-4"
          >
            Reset Password
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="email" // Input type should be 'email'
                name="useremailid"
                className="form-control"
                placeholder="Email Address"
                value={useremailid}
                onChange={handleChange}
                required
              />
            </div>
            <div
              className="mb-3"
              style={{
                position: "relative",
                display: "flex",
                alignItems: "center",
                margin: "10px auto",
                width: "100%",
              }}
            >
              <input
                type={showNewPassword ? "text" : "password"}
                name="NewPassword"
                className="form-control"
                placeholder="New Password"
                value={NewPassword}
                onChange={handleChange}
                required
                style={{ padding: "10px", width: "100%" }}
              />
              {NewPassword.length > 0 && (
                <FontAwesomeIcon
                  icon={showNewPassword ? faEyeSlash : faEye}
                  onClick={toggleNewPasswordVisibility}
                  style={{
                    position: "absolute",
                    right: "10px",
                    cursor: "pointer",
                  }}
                />
              )}
            </div>
            <div
              className="mb-3"
              style={{
                position: "relative",
                display: "flex",
                alignItems: "center",
                margin: "10px auto",
                width: "100%",
              }}
            >
              <input
                type={showConfirmPassword ? "text" : "password"}
                name="ConfirmPassword"
                className="form-control"
                placeholder="Confirm Password"
                value={ConfirmPassword}
                onChange={handleChange}
                required
                style={{ padding: "10px", width: "100%" }}
              />
              {ConfirmPassword.length > 0 && (
                <FontAwesomeIcon
                  icon={showConfirmPassword ? faEyeSlash : faEye}
                  onClick={toggleConfirmPasswordVisibility}
                  style={{
                    position: "absolute",
                    right: "10px",
                    cursor: "pointer",
                  }}
                />
              )}
            </div>

            {errors && <p style={{ color: "red" }}>{errors}</p>}
            {message && <p style={{ color: "green" }}>{message}</p>}
            <div className="d-flex justify-content-center">
              <Button
                style={buttonHoverStyle}
                type="submit"
                class="btn btn-primary btn-lg"
              >
                Reset Password
              </Button>
            </div>
          </form>
        </Col>
      </Row>
    </Container>
  );
}

export default ResetPasswordAdmin;
