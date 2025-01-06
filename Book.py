import streamlit as st
import mysql.connector 
import pandas as pd 
st.title(''':red[***Welcome to BookScape Explorer***]''')
# MySQL database connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",         # Replace with your host
        user="root",              # Replace with your MySQL username
        password="12345",         # Replace with your MySQL password
        database="bookscape"  # Replace with your database name
    )

# Function to execute SQL query and return results
def execute_sql_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)  # Execute the actual query
        result = cursor.fetchall()  # Fetch all the results
        columns = cursor.description  # Get column names
        # Convert to a Pandas DataFrame
        df = pd.DataFrame(result, columns=[col[0] for col in columns])
        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# Multi-select options
selected_options = st.multiselect(
    "Select the queries to execute",
    [
        "1.Check Availability of eBooks vs Physical Books",
        "2.Find the Publisher with the Most Books Published",
        "3.Identify the Publisher with the Highest Average Rating",
        "4.Get the Top 5 Most Expensive Books by Retail Price",
        "5.Find Books Published After 2010 with at Least 500 Pages",
        "6.List Books with Discounts Greater than 20%",
        "7.Find the Average Page Count for eBooks vs Physical Books",
        "8.Find the Top 3 Authors with the Most Books",
        "9.List Publishers with More than 10 Books",
        "10.Find the Average Page Count for Each Category",
        "11.Retrieve Books with More than 3 Authors",
        "12.Books with Ratings Count Greater Than the Average",
        "13.Books with the Same Author Published in the Same Year",
        "14.Books with a Specific Keyword in the Title",
        "15.Year with the Highest Average Book Price",
        "16.Count Authors Who Published 3 Consecutive Years",
        "17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year",
        "18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries",
        "19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers",
        "20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published"
    ]
)

# Function to generate SQL queries based on selected options
def generate_query(option):
    if option == "1.Check Availability of eBooks vs Physical Books":
        return """
       SELECT book_type, COUNT(*) AS book_count
        FROM books
        GROUP BY book_type;

        """
    elif option == "2.Find the Publisher with the Most Books Published":
        return """
       SELECT publisher, COUNT(*) AS book_count
FROM books
GROUP BY publisher
ORDER BY book_count DESC
LIMIT 1;
        """
    elif option == "3.Identify the Publisher with the Highest Average Rating":
        return """
       SELECT publisher, AVG(average_rating) AS avg_rating
FROM books
GROUP BY publisher
ORDER BY avg_rating DESC
LIMIT 1;

        """
    elif option == "4.Get the Top 5 Most Expensive Books by Retail Price":
        return """
       SELECT title, list_price_amount
FROM books
ORDER BY list_price_amount DESC
LIMIT 5;
        """
    elif option == "5.Find Books Published After 2010 with at Least 500 Pages":
        return """
       SELECT title, published_date, page_count
FROM books
WHERE published_date > 2010 AND page_count >= 500;

        """
    elif option == "6.List Books with Discounts Greater than 20%":
        return """
       SELECT title,  list_price_amount,retail_price_amount
FROM books
WHERE (list_price_amount-retail_price_amount) / list_price_amount > 0.20;
        """
    elif option == "7.Find the Average Page Count for eBooks vs Physical Books":
        return """
        SELECT book_type, AVG(page_count) AS avg_page_count
FROM books
GROUP BY book_type;
        """
    elif option == "8.Find the Top 3 Authors with the Most Books":
        return """
       SELECT authors, COUNT(*) AS book_count
FROM books
GROUP BY authors
ORDER BY book_count DESC
LIMIT 3;
        """
    elif option == "9.List Publishers with More than 10 Books":
        return """
       SELECT publisher, COUNT(*) AS book_count
FROM books
GROUP BY publisher
HAVING COUNT(*) > 10;
        """
    elif option == "10.Find the Average Page Count for Each Category":
        return """
      SELECT categories, AVG(page_count) AS avg_page_count
FROM books
GROUP BY categories;
        """
    elif option == "11.Retrieve Books with More than 3 Authors":
        return """
    SELECT title, authors
FROM books
WHERE ratings_count > 3;

        """
    elif option == "12.Books with Ratings Count Greater Than the Average":
        return """
      SELECT title, ratings_count
FROM books
WHERE ratings_count > (SELECT AVG(ratings_count) FROM books);
        """
    elif option == "13.Books with the Same Author Published in the Same Year":
        return """
      SELECT authors, published_date, COUNT(*) AS book_count
FROM books
GROUP BY authors, published_date
HAVING COUNT(*) > 1;
        """
    elif option == "14.Books with a Specific Keyword in the Title":
        return """
      SELECT title
FROM books
WHERE title LIKE '%Python For Dummies%';

        """
    elif option == "15.Year with the Highest Average Book Price":
        return """
      SELECT published_date, AVG(retail_price_amount) AS avg_price
FROM books
GROUP BY published_date
ORDER BY avg_price DESC
LIMIT 1;
        """
    elif option == "16.Count Authors Who Published 3 Consecutive Years":
        return """
      SELECT authors, COUNT(DISTINCT published_date) AS page_count
FROM books
GROUP BY authors
HAVING page_count >= 3;
        """
    elif option == "17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year":
        return """
      SELECT authors, published_date, COUNT(DISTINCT publisher) AS page_count
FROM books
GROUP BY authors, published_date
HAVING page_count > 1;
        """
    elif option == "18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries":
        return """
      SELECT
    AVG(CASE WHEN book_type = 'eBook' THEN retail_price_currency END) AS avg_ebook_price,
    AVG(CASE WHEN book_type = 'Physical' THEN retail_price_currency END) AS avg_physical_price
FROM books;
        """
    elif option == "19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers":
        return """
      SELECT title, average_rating, ratings_count
FROM books
WHERE ABS(average_rating - (SELECT AVG(average_rating) FROM books)) > 2 * (SELECT STDDEV(average_rating) FROM books);
        """
    elif option == "20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published":
        return """
      
SELECT publisher, AVG(average_rating) AS avg_rating, COUNT(*) AS book_count
FROM books
GROUP BY publisher
HAVING COUNT(*) > 10
ORDER BY avg_rating DESC
LIMIT 1;
        """
    
    return None

# Execute the SQL queries for selected options
if st.button("Execute SQL Queries"):
    for option in selected_options:
        query = generate_query(option)
        
        if query:
            st.write(f"Executing query for: {option}")
            df = execute_sql_query(query)  # Execute the actual query
            
            st.dataframe(df)  # Display results as a DataFrame
        else:
            st.warning(f"No query defined for {option}")


