# Street View Data Collector

This project provides a complete, end-to-end Python solution for collecting, organizing, and managing street-level imagery from the Google Street View Static API. It's designed for developers and researchers who need a structured dataset for computer vision tasks like analyzing urban infrastructure, sidewalks, or road conditions.

### 🌟 Features

  * **Automated Data Collection:** Downloads images programmatically from the Google Street View API.
  * **Customizable Routes:** Reads road and route data from a user-friendly CSV file.
  * **Automatic Heading Calculation:** Calculates the "forward" heading for each route to ensure images are consistently aligned.
  * **Organized Storage:** Stores images in a clean, hierarchical folder structure based on route names.
  * **Data Manifest:** Creates a detailed CSV log of every downloaded image with its metadata, making it easy to use the data in a Jupyter notebook or for further analysis.
  * **Robust Error Handling:** Manages API errors gracefully, logging failed requests without crashing the script.

### 🚀 Getting Started

Follow these steps to set up and run the project.

#### 1\. Prerequisites

You'll need a **Google Cloud Platform (GCP) account** and a valid API key for the **Street View Static API**. You can enable the API and get a key from your GCP console.

#### 2\. Installation

Clone this repository and install the required Python libraries.

```bash
git clone <repository_url>
cd street-view-data-collector
pip install -r requirements.txt
```

#### 3\. Setup

The project uses a simple folder structure for clarity.

  * `create_sample_csv.py`: Use this script to generate a sample input file.
  * `streetview_collector.py`: The main script that runs the collection process.
  * `routes.csv`: The input file where you define your routes.
  * `data/`: The output directory where all images and log files will be saved.

#### 4\. Usage

To begin, you can create a sample CSV to see how the project works.

**Step A: Create a Sample `routes.csv`**

Run the following command to generate a `routes.csv` with example data.

```bash
python create_sample_csv.py
```

**Step B: Add Your API Key**

Open the `streetview_collector.py` file and replace `"YOUR_API_KEY"` with your actual API key.

```python
# In streetview_collector.py
API_KEY: str = "YOUR_API_KEY"
```

**Step C: Run the Collector**

Execute the main script. It will read the routes from the CSV, download the images, and organize them into the `data/` folder.

```bash
python streetview_collector.py
```

After the script completes, you will find your images in `data/street_view_images/` and a `downloaded_images_log.csv` file that you can use to manage your dataset.

### 🛠️ Project Structure

```
.
├── create_sample_csv.py
├── streetview_collector.py
├── routes.csv
└── data/
    ├── street_view_images/
    │   ├── <route_name>/
    │   └── <route_name>/
    └── downloaded_images_log.csv
```