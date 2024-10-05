# Spark - Student Plagiarism Assignment Review Kit
### A plagiarism checker for comparing source code files and other documents. Mainly used for academic purposes to detect plagiarism in student assignments.

Spark is a Python-based desktop application that allows users to compare multiple source code files (or other documents) and calculate the similarity percentage between them. The application also provides suggestions for score deduction if the plagiarism level exceeds a predefined threshold.

## Key Features

- **Support for multiple file formats:** Compatible with `.txt`, `.pdf`, `.docx`, as well as various programming code files like `.py`, `.java`, `.cpp`, and more.
- **Similarity Percentage Calculation:** Compares the text from two or more files and computes the similarity percentage.
- **Score Deduction Recommendations:** If the file similarity exceeds the predefined threshold, the application suggests score deductions.
- **Export Results:** You can export the check results into an Excel file (`.xlsx`), which includes detailed similarity comparisons and score deduction recommendations.
- **Modern User Interface:** Built using `CustomTkinter` to provide a sleek and intuitive user interface.

## Screenshots
<div style="display: flex; flex-wrap: wrap; justify-content: center;">
  <div>
    <h3>Home</p>
    <img src="https://github.com/alfikiafan/plagiarism-checker/blob/main/resources/img/main-window.png" alt="Main Window" width="600">
  </div>
  <div>
    <h3>Plagiarism Check Results with Clusters</p>
    <img src="https://github.com/alfikiafan/plagiarism-checker/blob/main/resources/img/results.png" alt="Plagiarism Check Results with Clusters" width="600">
  </div>
  <div>
    <h3>File Comparison</p>
    <img src="https://github.com/alfikiafan/plagiarism-checker/blob/main/resources/img/comparison.png" alt="File Comparison" width="600">
  </div>
  <div>
    <h3>Check File Contents</p>
    <img src="https://github.com/alfikiafan/plagiarism-checker/blob/main/resources/img/file-contents.png" alt="Check File Contents" width="600">
  </div>
</div>

## System Requirements

Ensure you have the following before running the application:

- **Python 3.7+**
- Required Python modules (see the [Installation](#installation) section)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/alfikiafan/plagiarism-checker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd plagiarism-checker
   ```

3. Install all necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. Start the application by running:

   ```bash
   python main.py
   ```

2. **Steps within the application:**
   - Select two or more files to compare by clicking the `Browse` button.
   - Enter the similarity threshold percentage and the maximum score deduction (default is 80% similarity and 20% deduction).
   - Choose the output file location using the `Browse` button in the output section.
   - Click the `Start Check` button to begin the file comparison process.
   - The application will display the comparison results, suggest score deductions, and save the output to the specified Excel file.

## Project Structure

Here is the folder structure of the project:

```
├── controller/
│   ├── plagiarism_controller.py
├── model/
│   ├── file_reader.py
│   ├── plagiarism_checker.py
├── view/
│   ├── comparison_display.py
|   ├── file_content_display.py
|   ├── file_selection.py
|   ├── main_window.py
|   ├── results_display.py
├── utils/
│   ├── __init__.py
│   ├── constants.py
├── main.py
├── requirements.txt
└── README.md
```

- **`controller/`:** Contains the application's control logic, including file processing and coordination between the view and model.
- **`model/`:** Handles file reading and plagiarism checking logic.
- **`view/`:** Provides the user interface, built using `CustomTkinter`.
- **`utils/`:** Contains helper functions used throughout the application.
- **`main.py`:** The entry point of the application.

## Dependencies

The application relies on several Python libraries. These are listed in `requirements.txt`:

- **customtkinter**: For creating a modern-looking GUI based on Tkinter.
- **python-docx**: For reading `.docx` files.
- **pdfplumber**: For reading `.pdf` files.
- **pandas**: For data manipulation and exporting results to Excel.
- **openpyxl**: For writing data to Excel files.

## Example Excel Output

Once the plagiarism check is complete, the generated Excel file will contain two main sheets:

1. **Score Deduction:** Displays the percentage of score deductions based on file similarity.
2. **Similarity:** Shows the similarity percentage between the compared files.

## Contribution

Contributions are welcome! To contribute to this project:

1. Fork this repository.
2. Create a new feature branch (`git checkout -b new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or suggestions, feel free to reach out to me at [alfiki.diastama@gmail.com](mailto:alfiki.diastama@gmail.com).