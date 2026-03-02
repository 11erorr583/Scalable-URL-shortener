
## URL shortener with analytics engine
# Description:
 This is the URL shortner API that uses shoert code to redirect to the original url, this also have analytics tracking that generate API for tracking of each time short_url is clicked that includes os, browser, referrer, timestamp.
 **technologies_used**
 I used FastAPI, sqlite(SQLalchemy), pytest for unit testing and pydantic models for validation
 **key_features**
 - It supports features like have an expiry date feature,
 - tracking analytics api per click, custom short code(optional), 
 - autogenerate short code if null, 
 - and optional expiry date

# Installation

- **Clone the repository**  
   `git clone https://github.com/11erorr583/Scalable-URL-shortener.git`

- **Create the virtual environment**  
  In the root folder of the project:  
  `venv\Scripts\activate`  (Windows)  
  or  
  `source venv/bin/activate`  (Linux/Mac)

- **Install dependencies**  
  `pip install -r requirements.txt`

- **Set environment variables**  
  Save `.env.example` as `.env`  
  Example:  
     DATABASE_URL=sqlite:///./production.db
     BASE_URL=http://localhost:9000
  
  
- **Start the application**  
`uvicorn app.main:app --reload`  
This will start the server. Open Swagger UI at:  
http://localhost:9000/docs

# Syestem design choise:
**High level architecture**
- The client sends an HTTP request to the fastapi server
- the http request are handled by router
- this uses helper function i.e; code_generation(), masked_ip() etc
- to interact with database this uses sqlalchemy orm (object relational model)
- while the url and tracking analytics data is stored into the model
i.e; URL and Tracking
- schemas are used by API to generate and accept response

**Framework choise**
Framework: FastAPI
- fast than other framework like flask
- automatically perform validation using pydantic
- automatic API documentation 
   swaggerUI (/doc)
   ReDoc (/redoc)
   many frameworks need extra libraries for this
- FastAPI is designed for API, hence minimal overhead

# Database choise
Database: sqlite
- Lightweight, easy to configure
- works well for small to medium projects
- no extra database server
- file based database easy to configure

# Database Design Decisions
- the seprate model is used for URL to maintain normalization
- the tracking analytics data is stored in Tracking model
- indexing is used for short_code which is frequently accessed attribute to optimize retrievel
- one to many (back_populates=Tracking) is established between two data models
  as one URL can have multiple tracking data

# short code generation strategy
- The short code is generated for fixed number of symbols
  i.e; 6 as this is industry standard for URL short code
- only digits and alphabets are used in short code as special characters may have certain meaning in url
- if the custom short code is not entered by user this function automatically generates short_code.

# Security considerations
- rate limiting is applied one IP can request for 10 short_url generation per minute
  for this I used Limiter , _rate_limit_exceed_handeler from slowapi
- IP masking to applied before storing the ip into the database
- SQL injection is prevented by using SQL Alchemy ORM instead of sqlite Queries
- input validation is performed automatically by using pydantic
- sensitive configuration values are stored in .env file and added to .gitignore

# trade-offs
- the database chosen is sqlite for simplicity but limit concurrent write.
- built in rate limiting reduces complexity but not suitable for distributes database
- the constant small length of short_code may have collision risk.






