import path from "path";
import dotenv from "dotenv";
import fs from "fs";
import axios from "axios";

dotenv.config();

const playwright_folder = process.env.PLAYWRIGHT_FOLDER;
const report_folder = process.env.REPORT_FOLDER;
const screenshot_zip_folder = process.env.SCREENSHOT_ZIP_FOLDER;

export const downloadReport = (req, res) => {
  const { user_id } = req.params;
  const report_path = `${report_folder}/${user_id}/execution_report.html`;
  if (fs.existsSync(`${report_path}`)) {
    res.download(report_path, "Report.html", (err) => {
      if (err) {
        console.error("Error sending the report file:", err);
        res.status(500).send("Failed to send the file.");
      }
    });
  } else {
    res.status(404).send("Report file not found.");
  }
};

export const downloadScreenshotZip = (req, res) => {
  const { user_id } = req.params;
  const user_zip_path = `${screenshot_zip_folder}/${user_id}.zip`;
  if (fs.existsSync(user_zip_path)) {
    res.download(user_zip_path, "screenshots.zip", (err) => {
      if (err) {
        console.error("Error sending the screenshot zip file:", err);
        res.status(500).send("Failed to send the file.");
      }
    });
  } else {
    res.status(404).send("Report file not found.");
  }
};

// Trigger the Robot Framework process
export const triggerRobo = (req, res) => {
  const env = req.body["env"];
  const user_id = req.body["user_id"];
  const template = req.body["testCases"][0];

  console.log("Environment:", env, "User ID:", user_id, "Template", template);

  const uploaded_files_path = process.env.UPLOADS_DIR;

  const filePattern = new RegExp(`^${env}_${user_id}_\\d+_.*\\.xlsx$`); // Pattern to match files
  let recentFile = null;
  let recentTimestamp = 0;

  // Read all files in the uploads directory
  fs.readdir(uploaded_files_path, async (err, files) => {
    if (err) {
      console.error("Error reading uploads directory:", err);
      return res
        .status(500)
        .json({ error: "Unable to read uploads directory." });
    }

    // Filter for files that match the pattern
    const matchedFiles = files.filter((file) => filePattern.test(file));
    console.log("Matched files:", matchedFiles);

    // Find the most recent file based on the timestamp extracted from the filename
    matchedFiles.forEach((file) => {
      const [, , timestamp] = file.split("_"); // Extract timestamp
      const fileTimestamp = parseInt(timestamp, 10); // Convert to number

      if (fileTimestamp > recentTimestamp) {
        recentTimestamp = fileTimestamp;
        recentFile = file;
      }
    });

    if (!recentFile) {
      console.error("No matching files found for environment and user ID.");
      return res.status(404).json({ error: "No matching files found." });
    }

    const excel_file_path = path.join(uploaded_files_path, recentFile); // Full path of the latest file

    const flaskServerUrl = "http://localhost:3003/run-robot";

    try {
      const response = await axios.post(flaskServerUrl, {
        excel_file_path,
        env,
        user_id,
        shell_path: playwright_folder,
      });

      res.status(200).json({
        message: "Playwright executed.",
        data: response.data,
      });
    } catch (err) {
      console.error("Error triggering playwright: ", err);
      res.status(500).json({ error: "Failed to execute playwright" });
    }
  });
};
