import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();

// Default credentials
const adminCredentials = {
  email: "admin@its.jnj.com",
  password: "admin123",
};

// Login admin authentication
export const loginAdmin = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        message: "Please fill all mandatory fields.",
      });
    }

    // Checking for email pattern
    const emailPattern = /^[a-zA-Z0-9._]+@its\.jnj\.com$/;
    if (!emailPattern.test(email)) {
      return res.status(400).json({
        message: "Invalid email format. Please use a JNJ email (@its.jnj.com)",
      });
    }

    if (
      email !== adminCredentials.email ||
      password !== adminCredentials.password
    ) {
      return res.status(400).json({
        message: "Invalid credentials. Please try again.",
      });
    }

    // Generating token
    const token = jwt.sign(
      { email: adminCredentials.email },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );

    res.json({
      token,
      user: { email: adminCredentials.email },
    });
  } catch (err) {
    console.error("Admin login error: ", err);
    res.status(500).json({ message: "Server Error. Please try again later." });
  }
};
