# Project Title

Music Downloader

## Description

Online Music Downloading Tool  
Developed by Kayden Chung  

### Setup

* Clone the Repository
```
git clone https://github.com/KaydenChung/MusicDownloader.git
```
* Allow Windows to Run Scripts
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
* Create Virtual Environment
```
python -m venv .venv
```
* Activate Virtual Environment
#### Windows:
```
.venv\Scripts\activate
```
#### MacOS and Linux:
```
source .venv/bin/activate
```

### Execution

* Install Required Dependencies
```
pip install -r requirements.txt
```
* Run the Flask App
```
flask --app flaskr:app run --debug
```

