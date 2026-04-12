# TierStudio - NoSQL Database Implementation

**TierStudio** is a web-based, interactive ranking application designed to facilitate community-driven data collection and consensus-building. It allows users to create fully customizable tier list templates, categorize items via a drag-and-drop interface, and submit their individual rankings. 

This project was developed as a technical implementation of a **NoSQL Database Architecture**, specifically demonstrating the advantages of document-oriented data storage over traditional relational SQL databases.

## 🚀 Key Features
* **Custom Tier Lists:** Users can create custom ranking templates with unique tier names and item pools.
* **Drag-and-Drop Interface:** Intuitive UI for placing items into tiers.
* **Real-time NoSQL CRUD Operations:**
  * **Create:** Submitting new custom tier templates or user rankings to the database.
  * **Read:** Fetching templates and dynamic tier structures via API.
  * **Update:** Real-time state synchronization using PUT requests to update embedded document arrays.
  * **Delete:** Secure removal of parent documents and all embedded sub-data.
* **Community Consensus (Reporting):** Uses the **MongoDB Aggregation Pipeline** to analyze thousands of anonymous user submissions and calculate the statistical mode/vote count for item placements.

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla DOM API)
* **Backend:** Python, Flask
* **Database:** MongoDB (NoSQL Document Database)

## 📦 Installation and Setup
To run this project locally, you will need Python installed and a MongoDB connection (local or Atlas).

**1. Clone the repository**

    git clone https://github.com/YourUsername/TierStudio.git
    cd TierStudio

**2. Install dependencies**
Make sure you are in the project folder, then run:

    pip install flask pymongo flask-cors

**3. Start the server**

    python app.py

*(Note: If your main Python file is named something else, like server.py, replace app.py with your exact file name).*

The application will be running at http://localhost:5000.

## 🧠 Why NoSQL?
This application leverages a single-collection pattern with embedded arrays. Because NoSQL is schema-less, it easily loads custom tier categories without any relational constraints. This eliminates the need for complex, computationally heavy JOIN operations required in traditional SQL databases, making read and write operations extremely fast and highly scalable for a high-write "kiosk" environment.

## 👥 Team Members
* Pakapon Tasanaset
* Pakkapol Maluangnont
* Thanutch Mel Pholsukcharoen
* Phunyaphat Vijitrapornphan
* Tanadol Wonglerdsiri
* Nattaporn Lamwang

***

Note: Don't forget to change YourUsername in the Git Clone link to your actual GitHub username!