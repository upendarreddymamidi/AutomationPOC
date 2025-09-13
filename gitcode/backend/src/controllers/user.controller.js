import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
import {
  createUser,
  getUserByEmail,
  resetUserPassword,
  deleteUserById,
  getUsers,
} from "../models/user.js"; // Import functions

dotenv.config();

const generateUniqueId = () => {
  const min = 10; // Minimum 10-digit integer
  const max = 1000; // Maximum value for a 32-bit signed integer
  return Math.floor(Math.random() * (max - min + 1)) + min; // To generate a unique integer
};

export const signupUser = async (req, res) => {
  const { email, password, fullName } = req.body;

  // Check if email is in the correct format
  const emailPattern = /^[a-zA-Z0-9._%+-]+@its\.jnj\.com$/;
  if (!emailPattern.test(email)) {
    return res.status(400).json({ message: "Invalid email format." });
  }

  try {
    const existingUser = await getUserByEmail(email);
    if (existingUser) {
      return res.status(400).json({ message: "Email already in use." });
    }
    const id = generateUniqueId(); // Generate a unique integer identifier
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = await createUser({
      id,
      username: fullName,
      email,
      password_hash: hashedPassword,
    });

    res.status(201).json({
      message: "User registered successfully",
      user: {
        username: newUser.username,
        email: newUser.useremailid,
        createdAt: newUser.created_at,
      },
    });
  } catch (err) {
    console.error("Signup error:", err);
    res.status(500).json({ message: "Server error." });
  }
};

export const loginUser = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await getUserByEmail(email);
    if (!user) {
      return res.status(400).json({ message: "Invalid credentials." });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
      return res.status(400).json({ message: "Invalid credentials." });
    }

    const token = jwt.sign(
      { userId: user.user_id, email: user.useremailid },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );

    res.json({
      token,
      user: {
        id: user.user_id,
        username: user.username,
        email: user.useremailid,
        createdAt: user.created_at,
      },
    });
  } catch (err) {
    console.error("Login error:", err);
    res.status(500).json({ message: "Server error." });
  }
};

export const updatePassword = async (req, res) => {
  const { email, newPassword } = req.body;

  if (!email || !newPassword) {
    return res
      .status(400)
      .json({ error: "Email and new password are required." });
  }

  try {
    // Call the function to reset the user's password
    await resetUserPassword(email, newPassword);
    return res
      .status(200)
      .json({ message: "Your password has been reset successfully." });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
};

export const deleteUser = async (req, res) => {
  const { id } = req.params;
  try {
    const deletedUser = await deleteUserById(id); // Call the model function
    console.log(deletedUser);
    res.status(204).send(); // No content to return
  } catch (error) {
    console.error("Error deleting user:", error.message);
    return res.status(500).send("Server Error");
  }
};

export const getAllUsers = async (req, res) => {
  try {
    const users = await getUsers(); // Fetch users from model
    res.status(200).json(users); // Send user data as a JSON response
  } catch (error) {
    console.error("Error fetching users:", error.message);
    res.status(500).send("Server Error");
  }
};
