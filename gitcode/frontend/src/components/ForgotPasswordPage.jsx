import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState("");
  const [NewPassword, setNewPassword] = useState("");
  const [ConfirmPassword, setConfirmPassword] = useState("");
  const [showNewPassword, setNewShowPassword] = useState(false);
  const [showConfirmPassword, setConfirmShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [focus, setFocus] = useState({
    email: false,
    NewPassword: false,
    ConfirmPassword: false,
  });

  const buttonStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "email") setEmail(value);
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

    if (!email || !NewPassword || !ConfirmPassword) {
      setErrors("Email and Password are required.");
      return;
    }

    const emailPattern = /^[a-zA-Z0-9._%+-]+@its\.jnj\.com$/;
    if (!emailPattern.test(email)) {
      setErrors("Email must be a valid JNJ email.");
      return;
    }

    if (email === "admin@its.jnj.com") {
      setErrors("Admin is not allowed to change the password.");
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
          body: JSON.stringify({ email, newPassword: NewPassword }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setErrors("");
        setMessage(data.message);
        navigate("/login");
      } else {
        setErrors(data.error);
      }
    } catch (error) {
      setErrors("Failed to reset password. Please try again later.");
    }
  };

  const handleFocus = (field) => {
    setFocus({ ...focus, [field]: true });
  };

  const handleBlur = (field) => {
    setFocus({ ...focus, [field]: false });
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
                type="email"
                name="email"
                className="form-control"
                placeholder="Email Address"
                value={email}
                onChange={handleChange}
                onFocus={() => handleFocus("email")}
                onBlur={() => handleBlur("email")}
                required
                style={{
                  border: focus.email ? "2px solid black" : "1px solid #ced4da",
                  boxShadow: focus.email ? "0 0 1px black" : "none",
                  outline: "none",
                }}
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
                onFocus={() => handleFocus("NewPassword")}
                onBlur={() => handleBlur("NewPassword")}
                required
                style={{
                  border: focus.NewPassword
                    ? "2px solid black"
                    : "1px solid #ced4da",
                  boxShadow: focus.NewPassword ? "0 0 1px black" : "none",
                  outline: "none",
                }}
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
                onFocus={() => handleFocus("ConfirmPassword")}
                onBlur={() => handleBlur("ConfirmPassword")}
                required
                style={{
                  border: focus.ConfirmPassword
                    ? "2px solid black"
                    : "1px solid #ced4da",
                  boxShadow: focus.ConfirmPassword ? "0 0 1px black" : "none",
                  outline: "none",
                }}
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
                style={buttonStyle}
                type="submit"
                className="btn btn-primary btn-lg"
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

export default ForgotPasswordPage;
