import express from "express";
import {
  downloadReport,
  triggerRobo,
  downloadScreenshotZip,
} from "../controllers/robot.controller.js";

const router = express.Router();

router.post("/trigger-robot", triggerRobo);
router.get("/download-report/:user_id", downloadReport);
router.get("/download-zip/:user_id", downloadScreenshotZip);

export default router;
