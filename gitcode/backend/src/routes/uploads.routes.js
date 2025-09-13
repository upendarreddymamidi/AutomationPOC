import express from "express";
import { uploadFile } from "../controllers/uploads.controller.js"; // Adjust the path as necessary

const router = express.Router();

router.post("/:env/:user_id", uploadFile);

export default router;
