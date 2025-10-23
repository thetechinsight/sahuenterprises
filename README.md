# 📄 GSTR-5 Summary Generator

A Streamlit-based web application for generating GST Return Form 5 (GSTR-5) summaries from tax invoice files. This tool helps businesses automate the process of consolidating invoice data for GST compliance.

![Sahu Enterprises](https://img.shields.io/badge/Sahu-Enterprises-blue)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![GST](https://img.shields.io/badge/GST-Compliance-green)

## ✨ Features

- **Multi-file Upload**: Upload multiple Excel invoice files (.xls/.xlsx) simultaneously
- **Automated Data Extraction**: Intelligently extracts key invoice information including:
  - Date, Name, GSTIN, Invoice Number
  - HSN codes, quantities, taxable amounts
  - Tax calculations (18% GST)
  - Total amounts
- **Data Consolidation**: Groups and summarizes data by HSN codes
- **Excel Export**: Generates downloadable GSTR-5 summary in Excel format
- **User-friendly Interface**: Clean, branded Streamlit interface
- **Error Handling**: Robust error handling for various file formats and data issues

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (see requirements section)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thetechinsight/sahuenterprises.git
   cd sahuenterprises/gst-return-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit pandas openpyxl xlrd pathlib
   ```

3. **Run the application**:
   ```bash
   streamlit run gstr5.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:8501`

## 📋 Requirements

### Core Dependencies
```
streamlit
pandas
openpyxl
xlrd
pathlib
```

### Additional Requirements
- Ensure you have the `logo.png` file in the same directory as `gstr5.py`
- Excel files should follow the expected invoice format for proper data extraction

## 🔧 Usage

1. **Launch the Application**: Run the Streamlit app using the command above
2. **Upload Invoice Files**: 
   - Click on "Select Invoice Files"
   - Choose one or multiple Excel files (.xls or .xlsx)
   - Hold Ctrl (⌘ on Mac) to select multiple files
3. **Generate Summary**: Click the "🚀 Generate GSTR-5 Summary" button
4. **Review Data**: Check the generated summary table for accuracy
5. **Download**: Click "⬇️ Download GSTR-5 Summary" to save the Excel file

## 📊 Expected Invoice Format

The application expects Excel invoices with the following structure:
- **Header Information** (found by keyword matching):
  - Date
  - Name (Customer/Vendor name)
  - GSTIN (GST identification number)
  - Invoice No.
- **Item Details** (rows 19-60, columns C, E, I, N):
  - HSN Code (Column C)
  - Quantity (Column E)
  - Taxable Value (Column I)
  - Total Amount (Column N)

## 🏗️ Project Structure

```
gst-return-generator/
├── gstr5.py              # Main Streamlit application
├── logo.png              # Company logo
├── sahu_logo.png         # Additional logo
├── README.md             # This file
├── .gitignore           # Git ignore rules
└── temp/                # Temporary directory for file processing
```

## 💡 How It Works

1. **File Upload**: Users upload Excel invoice files through the web interface
2. **Data Extraction**: The app reads each Excel file and searches for:
   - Header information using keyword matching
   - Item details from predefined cell ranges
3. **Data Processing**: 
   - Cleans and validates numerical data
   - Groups items by HSN code
   - Calculates tax amounts (18% GST)
   - Sums quantities and amounts
4. **Summary Generation**: Creates a consolidated DataFrame with all invoice data
5. **Export**: Saves the summary as an Excel file for download

## 🛠️ Technical Details

### Key Functions

- `find_value_horizontal()`: Searches for keywords and extracts adjacent values
- `extract_invoice_data()`: Processes individual Excel files and extracts structured data
- `summarize_files()`: Consolidates data from multiple files

### Data Processing

- Handles both `.xls` and `.xlsx` formats
- Automatic date formatting (DD-MM-YYYY)
- Numerical data cleaning and validation
- HSN-based grouping and aggregation
- Tax calculation (18% GST rate)

## 🎨 Customization

### Styling
The application uses custom CSS for branding with Sahu Enterprises colors:
- Primary: `#4AAFD5` (Blue)
- Secondary: `#91B187` (Green)

### Logo
Replace `logo.png` with your company logo to customize the branding.

## 🐛 Troubleshooting

### Common Issues

1. **File Upload Errors**: Ensure Excel files are not corrupted and follow the expected format
2. **xlrd Engine Errors**: The app automatically falls back to xlrd engine for older Excel formats
3. **Missing Data**: Check if your invoice format matches the expected structure
4. **Logo Not Found**: Ensure `logo.png` exists in the application directory

### Error Messages

- **"Please upload at least one file"**: No files were selected for upload
- **"No valid data found"**: The uploaded files don't contain extractable data
- **File-specific warnings**: Individual file processing errors are displayed as warnings

## 📄 License

This project is part of Sahu Enterprises and is proprietary software.

## 👥 Contributing

For internal development and contributions, please follow the company's development guidelines.

## 📞 Support

For technical support or questions, please contact the development team at Sahu Enterprises.

---

**© 2025 Sahu Enterprises | Built with ❤️**

*This tool is designed to streamline GST compliance processes and reduce manual data entry errors in tax return preparation.*
