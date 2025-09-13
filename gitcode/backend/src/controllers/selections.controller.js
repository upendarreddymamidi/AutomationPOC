import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();

// Will replace with actual logic of fetching the names and testcases from database
const fetchApplicationNamesAndTestCases = async () => {
  return {
    applications: ["Workday"],
    environment: ["impl-jj15", "impl-jj1"],
    testCases: [
      "Hire",
      "Leave_of_Absence",
      "Return_from_Leave",
      "Termination",
      "One_Time_Payment",
      "Edit_Additional_Data",
      // "Acquisition_Mexico",
      "Compensation_Change",
      "Job_Change",
      "Change_Personal_Information",
    ],
  };
};

// POST - VALIDATING SELECTIONS
export const handleSelections = async (req, res) => {
  // Extracting toke from the authorization header
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  // Checking if the token is present
  if (!token) {
    return res
      .status(401)
      .json({ message: "Access Denied. No token provided" });
  }

  // Verifying the token
  try {
    jwt.verify(token, process.env.JWT_SECRET);
  } catch (err) {
    console.log(err);
    return res.status(403).json({ message: "Invalid token." });
  }

  // Getting data from selectionsPage.js
  const {
    application,
    environment,
    testCases,
    generateScreenshots,
    generateExcel,
  } = req.body;

  // Input Validation
  if (!application || !environment || testCases.length === 0) {
    return res.status(400).json({
      message:
        "Please provide all required fields : application, environment and at least one test case.",
    });
  }

  // Logging the data
  console.log("Received selections:", {
    application,
    environment,
    testCases,
    generateScreenshots,
    generateExcel,
  });

  // Sending a response back
  res.status(200).json({
    message: "Selections received successfully.",
    data: {
      application,
      environment,
      testCases,
      generateScreenshots,
      generateExcel,
    },
  });
};

// GET - GET APPLICATION NAMES AND TEST CASES
export const getData = async (req, res) => {
  // Extracting toke from the authorization header
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  // // Checking if the token is present
  if (!token) {
    return res
      .status(401)
      .json({ message: "Access Denied. No token provided" });
  }

  try {
    jwt.verify(token, process.env.JWT_SECRET);
  } catch (err) {
    console.log(err);
    return res.status(403).json({ message: "Invalid token." });
  }

  try {
    const data = await fetchApplicationNamesAndTestCases();
    return res.status(200).json({
      message: "Application names and test cases retrieved successfully.",
      data: data,
    });
  } catch (error) {
    console.log("Error fetching data: ", error);
    return res.status(500).json({
      message: "An error occurred while retrieving data.",
    });
  }
};
