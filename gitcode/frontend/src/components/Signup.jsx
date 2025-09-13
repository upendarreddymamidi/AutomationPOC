import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    fullName: "",
  });

  const [errors, setErrors] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [focus, setFocus] = useState({ email: false, password: false });

  const buttonStyle = {
    backgroundColor: "white",
    color: "#eb1700", // Red color
    border: "2px solid #eb1700", // Red border
    padding: "10px 20px",
    cursor: "pointer",
    transition: "background-color 0.3s, color 0.3s, border 0.3s",
    fontSize: "16px",
    height: "50px",

    outline: "none",
  };

  const buttonHoverStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  const [isHovered, setIsHovered] = useState(false);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errors) setErrors("");
  }

  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      setErrors("Email and Password are required.");
      return;
    }

    const emailPattern = /^[a-zA-Z0-9._%+-]+@its\.jnj\.com$/;
    if (!emailPattern.test(formData.email)) {
      setErrors("Email must be a valid JNJ email.");
      return;
    }

    setErrors("");

    try {
      const response = await fetch("http://localhost:9996/api/users/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrors(errorData.message || "Failed to sign up.");
      } else {
        const data = await response.json();
        console.log("Signup successful:", data);
        navigate("/login"); // Redirect or handle success
      }
    } catch (error) {
      setErrors("An error occurred while signing up.");
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
              display: "block",
              color: "#eb1700",
            }}
            className="text-center mb-4"
          >
            Sign Up
          </h2>
          <br></br>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="Username (JNJ email)"
                value={formData.email}
                onChange={handleChange}
                onFocus={() => handleFocus("email")}
                onBlur={() => handleBlur("email")}
                required
                style={{
                  border: focus.email ? "2px solid black" : "1px solid #ced4da",
                  boxShadow: focus.email ? "0 0 1px black" : "none",
                  outline: "none", // Removes the default outline
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
                type={showPassword ? "text" : "password"}
                name="password"
                className="form-control"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                onFocus={() => handleFocus("password")}
                onBlur={() => handleBlur("password")}
                required
                style={{
                  padding: "10px",
                  width: "100%",
                  border: focus.password
                    ? "2px solid black"
                    : "1px solid #ced4da",
                  boxShadow: focus.password ? "0 0 1px black" : "none",
                  outline: "none", // Removes the default outline
                }}
              />
              <FontAwesomeIcon
                icon={showPassword ? faEyeSlash : faEye}
                onClick={handlePasswordVisibility}
                style={{
                  position: "absolute",
                  right: "10px",
                  cursor: "pointer",
                }}
              />
            </div>

            {errors && <p style={{ color: "red" }}>{errors}</p>}
            <br></br>
            <div className="d-flex justify-content-center">
              <Button
                style={
                  isHovered
                    ? { ...buttonStyle, ...buttonHoverStyle }
                    : buttonStyle
                }
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                type="submit"
                class="btn btn-primary btn-lg"
              >
                Sign Up
              </Button>
            </div>
          </form>
        </Col>
      </Row>
    </Container>
  );
}

export default Signup;
