// backend/src/routes/user.routes.js
import express from "express";
import { loginUser, signupUser } from "../controllers/user.controller.js";
import { getAllUsers, deleteUser } from "../controllers/user.controller.js";

import { updatePassword } from "../controllers/user.controller.js";
const router = express.Router();



// Define the login route
router.post("/auth", loginUser);
router.post("/signup", signupUser);
// Route to fetch all users
router.get("/", getAllUsers);
router.post("/updatepwd", updatePassword);
router.delete("/:id", deleteUser); // delete user route

export default router;

