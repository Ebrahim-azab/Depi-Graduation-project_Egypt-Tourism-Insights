/* ============================================================================
   -- Data Cleaning 
   ============================================================================ */


CREATE DATABASE IF NOT EXISTS egypt_tourism;
USE egypt_tourism;
SET SQL_SAFE_UPDATES = 0; 


--  1: INITIAL EXPLORATION
-- ----------------------------------------------------------------------------
DESCRIBE main_data;
SELECT * FROM main_data LIMIT 10;
SELECT COUNT(*) AS total_rows FROM main_data;


--  2: DATA STANDARDIZATION & CLEANING
-- ----------------------------------------------------------------------------
-- 2.1: Trim leading/trailing spaces and convert empty strings to NULL
UPDATE main_data
SET 
    Fact_Key             = NULLIF(TRIM(Fact_Key), ''),
    Dest_Key             = NULLIF(TRIM(Dest_Key), ''),
    Country_Key          = NULLIF(TRIM(Country_Key), ''),
    Transport_Mode       = NULLIF(TRIM(Transport_Mode), ''),
    Purpose_of_Visit     = NULLIF(TRIM(Purpose_of_Visit), ''),
    Egypt_Tourism_Season = NULLIF(TRIM(Egypt_Tourism_Season), ''),
    Data_Type            = NULLIF(TRIM(Data_Type), ''),
    Entry_Point          = NULLIF(TRIM(Entry_Point), ''),
    Transport_Source     = NULLIF(TRIM(Transport_Source), '');
 
-- 2.2: Standardize Transport_Mode 
UPDATE main_data
SET transport_mode = CASE
    WHEN UPPER(transport_mode) = 'AIR'  THEN 'Air'
    WHEN UPPER(transport_mode) = 'LAND' THEN 'Land'
    WHEN UPPER(transport_mode) = 'SEA'  THEN 'Sea'
    ELSE transport_mode
END;
 
-- 2.3: Standardize Tourism Season
UPDATE main_data
SET egypt_tourism_season = CASE
    WHEN LOWER(egypt_tourism_season) = 'peak'     THEN 'Peak'
    WHEN LOWER(egypt_tourism_season) = 'shoulder' THEN 'Shoulder'
    WHEN LOWER(egypt_tourism_season) = 'low'      THEN 'Low'
    ELSE egypt_tourism_season
END;
 
-- 2.4: Standardize Purpose of Visit 
UPDATE main_data
SET purpose_of_visit = CASE
    WHEN LOWER(purpose_of_visit) = 'leisure'   THEN 'Leisure'
    WHEN LOWER(purpose_of_visit) = 'business'  THEN 'Business'
    WHEN LOWER(purpose_of_visit) = 'religious' THEN 'Religious'
    WHEN LOWER(purpose_of_visit) = 'cultural'  THEN 'Cultural'
    WHEN LOWER(purpose_of_visit) = 'transit'   THEN 'Transit'
    WHEN LOWER(purpose_of_visit) = 'medical'   THEN 'Medical'
    ELSE purpose_of_visit
END;

-- 2.5: Standardize Boolean logic for Nile_Cruise_Hub 
UPDATE dim_destination
SET Nile_Cruise_Hub = CASE
    WHEN LOWER(TRIM(Nile_Cruise_Hub)) = 'yes' THEN 1
    ELSE 0
END;

--  3: DATA QUALITY 
-- ----------------------------------------------------------------------------
-- 3.1: Check for fully identical rows
SELECT 
    fact_key, date_key, dest_key, country_key, transport_mode, 
    COUNT(*) AS cnt
FROM main_data
GROUP BY fact_key, date_key, dest_key, country_key, transport_mode
HAVING COUNT(*) > 1
ORDER BY cnt DESC;

-- 3.2: Check for duplicate 
SELECT fact_key, COUNT(*) AS cnt
FROM main_data
GROUP BY fact_key
HAVING COUNT(*) > 1;

-- 3.3: Count missing values (NULLs) 
SELECT
    SUM(fact_key IS NULL)              AS missing_fact_key,
    SUM(date_key IS NULL)              AS missing_date_key,
    SUM(year IS NULL)                  AS missing_year,
    SUM(month IS NULL)                 AS missing_month,
    SUM(dest_key IS NULL)              AS missing_dest_key,
    SUM(country_key IS NULL)           AS missing_country_key,
    SUM(tourist_arrivals IS NULL)      AS missing_tourist_arrivals,
    SUM(tourism_revenue_usd IS NULL)   AS missing_revenue,
    SUM(avg_spend_per_tourist_usd IS NULL) AS missing_avg_spend,
    SUM(hotel_occupancy_rate_pct IS NULL)  AS missing_occupancy,
    SUM(avg_stay_days IS NULL)         AS missing_stay_days,
    SUM(transport_mode IS NULL)        AS missing_transport_mode,
    SUM(purpose_of_visit IS NULL)      AS missing_purpose,
    SUM(adr_usd IS NULL)               AS missing_adr_usd,
    SUM(revpar_usd IS NULL)            AS missing_revpar_usd,
    SUM(usd_egp_rate IS NULL)          AS missing_fx_rate
FROM main_data;

-- STEP 4: STATISTICAL UNDERSTANDING & SUMMARY
-- ----------------------------------------------------------------------------
-- Create a comprehensive summary table for all numeric metrics
DROP TABLE IF EXISTS main_numeric_summary;
CREATE TABLE main_numeric_summary AS
SELECT 'Tourist_Arrivals' AS column_name, COUNT(*) AS row_count, MIN(Tourist_Arrivals) AS min_value, MAX(Tourist_Arrivals) AS max_value, ROUND(AVG(Tourist_Arrivals),2) AS avg_value, ROUND(STDDEV(Tourist_Arrivals),2) AS std_value FROM Main_Data
UNION ALL
SELECT 'Tourism_Revenue_USD', COUNT(*), MIN(Tourism_Revenue_USD), MAX(Tourism_Revenue_USD), ROUND(AVG(Tourism_Revenue_USD),2), ROUND(STDDEV(Tourism_Revenue_USD),2) FROM Main_Data
UNION ALL
SELECT 'Avg_Spend_Per_Tourist_USD', COUNT(*), MIN(Avg_Spend_Per_Tourist_USD), MAX(Avg_Spend_Per_Tourist_USD), ROUND(AVG(Avg_Spend_Per_Tourist_USD),2), ROUND(STDDEV(Avg_Spend_Per_Tourist_USD),2) FROM Main_Data
UNION ALL
SELECT 'Hotel_Occupancy_Rate_pct', COUNT(*), MIN(Hotel_Occupancy_Rate_pct), MAX(Hotel_Occupancy_Rate_pct), ROUND(AVG(Hotel_Occupancy_Rate_pct),2), ROUND(STDDEV(Hotel_Occupancy_Rate_pct),2) FROM Main_Data
UNION ALL
SELECT 'Hotel_Rooms_Destination', COUNT(*), MIN(Hotel_Rooms_Destination), MAX(Hotel_Rooms_Destination), ROUND(AVG(Hotel_Rooms_Destination),2), ROUND(STDDEV(Hotel_Rooms_Destination),2) FROM Main_Data
UNION ALL
SELECT 'Avg_Stay_Days', COUNT(*), MIN(Avg_Stay_Days), MAX(Avg_Stay_Days), ROUND(AVG(Avg_Stay_Days),2), ROUND(STDDEV(Avg_Stay_Days),2) FROM Main_Data
UNION ALL
SELECT 'Package_Tour_Share_pct', COUNT(*), MIN(Package_Tour_Share_pct), MAX(Package_Tour_Share_pct), ROUND(AVG(Package_Tour_Share_pct),2), ROUND(STDDEV(Package_Tour_Share_pct),2) FROM Main_Data
UNION ALL
SELECT 'Avg_Temp_C', COUNT(*), MIN(Avg_Temp_C), MAX(Avg_Temp_C), ROUND(AVG(Avg_Temp_C),2), ROUND(STDDEV(Avg_Temp_C),2) FROM Main_Data
UNION ALL
SELECT 'Active_Nile_Cruise_Boats', COUNT(*), MIN(Active_Nile_Cruise_Boats), MAX(Active_Nile_Cruise_Boats), ROUND(AVG(Active_Nile_Cruise_Boats),2), ROUND(STDDEV(Active_Nile_Cruise_Boats),2) FROM Main_Data
UNION ALL
SELECT 'Avg_Daily_Spend_USD', COUNT(*), MIN(Avg_Daily_Spend_USD), MAX(Avg_Daily_Spend_USD), ROUND(AVG(Avg_Daily_Spend_USD),2), ROUND(STDDEV(Avg_Daily_Spend_USD),2) FROM Main_Data
UNION ALL
SELECT 'ADR_USD', COUNT(*), MIN(ADR_USD), MAX(ADR_USD), ROUND(AVG(ADR_USD),2), ROUND(STDDEV(ADR_USD),2) FROM Main_Data
UNION ALL
SELECT 'RevPAR_USD', COUNT(*), MIN(RevPAR_USD), MAX(RevPAR_USD), ROUND(AVG(RevPAR_USD),2), ROUND(STDDEV(RevPAR_USD),2) FROM Main_Data
UNION ALL
SELECT 'ADR_EGP', COUNT(*), MIN(ADR_EGP), MAX(ADR_EGP), ROUND(AVG(ADR_EGP),2), ROUND(STDDEV(ADR_EGP),2) FROM Main_Data
UNION ALL
SELECT 'USD_EGP_Rate', COUNT(*), MIN(USD_EGP_Rate), MAX(USD_EGP_Rate), ROUND(AVG(USD_EGP_Rate),2), ROUND(STDDEV(USD_EGP_Rate),2) FROM Main_Data
UNION ALL
SELECT 'Avg_Flight_Cost_USD', COUNT(*), MIN(Avg_Flight_Cost_USD), MAX(Avg_Flight_Cost_USD), ROUND(AVG(Avg_Flight_Cost_USD),2), ROUND(STDDEV(Avg_Flight_Cost_USD),2) FROM Main_Data;
 
SELECT * FROM main_numeric_summary;


--  5: SCHEMA OPTIMIZATION
-- ----------------------------------------------------------------------------
-- Remove redundant columns handled by Date_Key
ALTER TABLE main_data 
DROP COLUMN Year, 
DROP COLUMN Month;



    -- 6:  DATA TYPE CORRECTION 
-- ----------------------------------------------------------------------------

ALTER TABLE dim_destination
    MODIFY COLUMN Dest_Key VARCHAR(50),
    MODIFY COLUMN Destination_Name VARCHAR(100),
    MODIFY COLUMN Region VARCHAR(100),
    MODIFY COLUMN Tourism_Type VARCHAR(100),
    MODIFY COLUMN Hotel_Rooms INT,
    MODIFY COLUMN Nile_Cruise_Hub TINYINT;


ALTER TABLE dim_country
    MODIFY COLUMN Country_Key VARCHAR(50),
    MODIFY COLUMN Country_Name VARCHAR(100),
    MODIFY COLUMN Region VARCHAR(100),
    MODIFY COLUMN Language VARCHAR(100);


ALTER TABLE dim_transport
    MODIFY COLUMN Transport_Mode VARCHAR(50),
    MODIFY COLUMN Entry_Type VARCHAR(100),
    MODIFY COLUMN Description VARCHAR(255),
    MODIFY COLUMN Flight_Cost_Applicable VARCHAR(20);


ALTER TABLE dim_purpose
    MODIFY COLUMN Purpose_of_Visit VARCHAR(50),
    MODIFY COLUMN Description VARCHAR(255),
    MODIFY COLUMN Typical_Stay_Length VARCHAR(50);


ALTER TABLE dim_entry_point
    MODIFY COLUMN Entry_Point VARCHAR(100),
    MODIFY COLUMN Entry_Type VARCHAR(100),
    MODIFY COLUMN Linked_Dest_Key VARCHAR(50);


ALTER TABLE dim_date
    MODIFY COLUMN Date_Key INT,
    MODIFY COLUMN Year INT,
    MODIFY COLUMN Month INT,
    MODIFY COLUMN Month_Name VARCHAR(50),
    MODIFY COLUMN Quarter INT,
    MODIFY COLUMN Egypt_Tourism_Season VARCHAR(50);


-- 6.2: FACT TABLE 
-- ----------------------------------------------------------------------------
ALTER TABLE main_data
    MODIFY COLUMN Fact_Key VARCHAR(100),
    MODIFY COLUMN Date_Key INT,
    MODIFY COLUMN Dest_Key VARCHAR(50),
    MODIFY COLUMN Country_Key VARCHAR(50),
    MODIFY COLUMN Transport_Mode VARCHAR(50),
    MODIFY COLUMN Purpose_of_Visit VARCHAR(50),
    MODIFY COLUMN Entry_Point VARCHAR(100),
    
    
    MODIFY COLUMN Tourist_Arrivals INT,
    MODIFY COLUMN Hotel_Rooms_Destination INT,
    MODIFY COLUMN Active_Nile_Cruise_Boats INT,
    MODIFY COLUMN Nile_Cruise_Hub TINYINT,
    
    
    MODIFY COLUMN Tourism_Revenue_USD DECIMAL(15, 2),
    MODIFY COLUMN Avg_Spend_Per_Tourist_USD DECIMAL(10, 2),
    MODIFY COLUMN Avg_Daily_Spend_USD DECIMAL(10, 2),
    MODIFY COLUMN ADR_USD DECIMAL(10, 2),
    MODIFY COLUMN RevPAR_USD DECIMAL(10, 2),
    MODIFY COLUMN ADR_EGP DECIMAL(10, 2),
    MODIFY COLUMN USD_EGP_Rate DECIMAL(10, 4),
    MODIFY COLUMN Avg_Flight_Cost_USD DECIMAL(10, 2),
    MODIFY COLUMN Hotel_Occupancy_Rate_pct DECIMAL(5, 2),
    MODIFY COLUMN Avg_Stay_Days DECIMAL(5, 2),
    MODIFY COLUMN Package_Tour_Share_pct DECIMAL(5, 2),
    MODIFY COLUMN Avg_Temp_C DECIMAL(5, 2),
    
    
    MODIFY COLUMN Egypt_Tourism_Season VARCHAR(50),
    MODIFY COLUMN Transport_Source VARCHAR(100);


-- 6.3: EXTERNAL DATA TABLES 
-- ----------------------------------------------------------------------------

ALTER TABLE exchange_rate_cbe
    MODIFY COLUMN Year INT,
    MODIFY COLUMN USD_EGP_Annual_Avg DECIMAL(10, 4),
    MODIFY COLUMN Source VARCHAR(255),
    MODIFY COLUMN Event VARCHAR(255);


ALTER TABLE competitor_data
    MODIFY COLUMN Year INT,
    MODIFY COLUMN Country VARCHAR(100),
    MODIFY COLUMN Arrivals_M DECIMAL(10, 2),
    MODIFY COLUMN Source VARCHAR(255),
    MODIFY COLUMN Egypt_Arrivals_M DECIMAL(10, 2),
    MODIFY COLUMN Egypt_Share_Of_5Markets_pct DECIMAL(5, 2);
    
    
    
-- 7  : OUTLIER DETECTION 
-- ----------------------------------------------------------------------------

-- 7.1: IQR Summary for Tourist Arrivals
WITH ranked_arrivals AS (
    SELECT 
        Dest_Key, Tourist_Arrivals,
        ROW_NUMBER() OVER (PARTITION BY Dest_Key ORDER BY Tourist_Arrivals) AS row_pos,
        COUNT(*)     OVER (PARTITION BY Dest_Key) AS total_rows
    FROM Main_Data
),
quartile_positions AS (
    SELECT 
        Dest_Key, Tourist_Arrivals, row_pos,
        CEIL(total_rows * 0.25) AS q1_pos,
        CEIL(total_rows * 0.75) AS q3_pos
    FROM ranked_arrivals
),
quartile_values AS (
    SELECT 
        Dest_Key,
        MAX(CASE WHEN row_pos = q1_pos THEN Tourist_Arrivals END) AS Q1,
        MAX(CASE WHEN row_pos = q3_pos THEN Tourist_Arrivals END) AS Q3
    FROM quartile_positions
    GROUP BY Dest_Key
)
SELECT 
    Dest_Key,
    Q1,
    Q3,
    (Q3 - Q1) AS IQR,
    ROUND(Q1 - 1.5 * (Q3 - Q1), 0) AS lower_bound,
    ROUND(Q3 + 1.5 * (Q3 - Q1), 0) AS upper_bound
FROM quartile_values
ORDER BY Dest_Key;

-- 7.2: IQR Summary for Average Stay Days
WITH ranked_stay AS (
    SELECT 
        Dest_Key, Avg_Stay_Days,
        ROW_NUMBER() OVER (PARTITION BY Dest_Key ORDER BY Avg_Stay_Days) AS row_pos,
        COUNT(*)     OVER (PARTITION BY Dest_Key) AS total_rows
    FROM Main_Data
),
quartile_positions AS (
    SELECT 
        Dest_Key, Avg_Stay_Days, row_pos,
        CEIL(total_rows * 0.25) AS q1_pos,
        CEIL(total_rows * 0.75) AS q3_pos
    FROM ranked_stay
),
quartile_values AS (
    SELECT 
        Dest_Key,
        MAX(CASE WHEN row_pos = q1_pos THEN Avg_Stay_Days END) AS Q1,
        MAX(CASE WHEN row_pos = q3_pos THEN Avg_Stay_Days END) AS Q3
    FROM quartile_positions
    GROUP BY Dest_Key
)
SELECT 
    Dest_Key,
    Q1,
    Q3,
    (Q3 - Q1) AS IQR,
    ROUND(Q1 - 1.5 * (Q3 - Q1), 2) AS lower_bound,
    ROUND(Q3 + 1.5 * (Q3 - Q1), 2) AS upper_bound
FROM quartile_values
ORDER BY Dest_Key;

-- 7.3: IQR Summary for Tourism Revenue (USD)
WITH ranked_revenue AS (
    SELECT 
        Dest_Key, Tourism_Revenue_USD,
        ROW_NUMBER() OVER (PARTITION BY Dest_Key ORDER BY Tourism_Revenue_USD) AS row_pos,
        COUNT(*)     OVER (PARTITION BY Dest_Key) AS total_rows
    FROM Main_Data
),
quartile_positions AS (
    SELECT 
        Dest_Key, Tourism_Revenue_USD, row_pos,
        CEIL(total_rows * 0.25) AS q1_pos,
        CEIL(total_rows * 0.75) AS q3_pos
    FROM ranked_revenue
),
quartile_values AS (
    SELECT 
        Dest_Key,
        MAX(CASE WHEN row_pos = q1_pos THEN Tourism_Revenue_USD END) AS Q1,
        MAX(CASE WHEN row_pos = q3_pos THEN Tourism_Revenue_USD END) AS Q3
    FROM quartile_positions
    GROUP BY Dest_Key
)
SELECT 
    Dest_Key,
    Q1,
    Q3,
    (Q3 - Q1) AS IQR,
    ROUND(Q1 - 1.5*(Q3 - Q1), 0) AS lower_bound,
    ROUND(Q3 + 1.5*(Q3 - Q1), 0) AS upper_bound
FROM quartile_values
ORDER BY Dest_Key;

-- Enable safe updates back for security
SET SQL_SAFE_UPDATES = 1;
-- ----------------------------------------------------------------------------
-- ----------------------------------------------------------------------------

   -- DATA MODELING 

ALTER TABLE dim_date ADD PRIMARY KEY (Date_Key);
ALTER TABLE dim_destination ADD PRIMARY KEY (Dest_Key);
ALTER TABLE dim_country ADD PRIMARY KEY (Country_Key);
ALTER TABLE dim_transport ADD PRIMARY KEY (Transport_Mode);
ALTER TABLE dim_purpose ADD PRIMARY KEY (Purpose_of_Visit);
ALTER TABLE dim_entry_point ADD PRIMARY KEY (Entry_Point);


ALTER TABLE main_data ADD PRIMARY KEY (Fact_Key);
-- 1. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_date FOREIGN KEY (Date_Key) REFERENCES dim_date(Date_Key);

-- 2. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_dest FOREIGN KEY (Dest_Key) REFERENCES dim_destination(Dest_Key);

-- 3. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_country FOREIGN KEY (Country_Key) REFERENCES dim_country(Country_Key);

-- 4. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_transport FOREIGN KEY (Transport_Mode) REFERENCES dim_transport(Transport_Mode);

-- 5. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_purpose FOREIGN KEY (Purpose_of_Visit) REFERENCES dim_purpose(Purpose_of_Visit);

-- 6. 
ALTER TABLE main_data 
ADD CONSTRAINT fk_main_entry FOREIGN KEY (Entry_Point) REFERENCES dim_entry_point(Entry_Point);

-- ----------------------------------------------------------------------------
-- ----------------------------------------------------------------------------
/* ============================================================================
   1- Tourism Trend Over the Years (2005–2024)
   ============================================================================ */
SELECT 
    d.Year,
    SUM(m.Tourist_Arrivals) AS Arrivals,
    SUM(m.Tourism_Revenue_USD) AS Revenue
FROM main_data m
JOIN dim_date d 
    ON m.Date_Key = d.Date_Key
GROUP BY 
    d.Year
ORDER BY 
    d.Year ASC;
    
/* ============================================================================
   2- Top 10 Source Countries by Revenue (in Billion USD)
   ============================================================================ */
SELECT 
    c.Country_Name,
    ROUND(SUM(m.Tourism_Revenue_USD) / 1000000000, 2) AS Revenue_Billion_USD
FROM main_data m
JOIN dim_country c 
    ON m.Country_Key = c.Country_Key
GROUP BY 
    c.Country_Name
ORDER BY 
    Revenue_Billion_USD DESC
LIMIT 10;

/* ============================================================================
   3- Destination Performance (Arrivals & Revenue by Destination)
   ============================================================================ */
SELECT 
    d.Destination_Name,
    SUM(m.Tourist_Arrivals) AS Arrivals,
    SUM(m.Tourism_Revenue_USD) AS Revenue
FROM main_data m
JOIN dim_destination d 
    ON m.Dest_Key = d.Dest_Key
GROUP BY 
    d.Destination_Name
ORDER BY 
    Revenue DESC;
    
/* ============================================================================
   4- Effect of Season on Arrivals (Arrivals by Quarter)
   ============================================================================ */
SELECT 
    d.Quarter,
    SUM(m.Tourist_Arrivals) AS Total_Arrivals
FROM main_data m
JOIN dim_date d 
    ON m.Date_Key = d.Date_Key
GROUP BY 
    d.Quarter
ORDER BY 
    d.Quarter ASC;
    
/* ============================================================================
   5- Arrivals Share by Transport Mode (Pie Chart Equivalent)
   ============================================================================ */
SELECT 
    t.Transport_Mode,
    SUM(m.Tourist_Arrivals) AS Total_Arrivals,
    ROUND((SUM(m.Tourist_Arrivals) / (SELECT SUM(Tourist_Arrivals) FROM main_data)) * 100, 0) AS Percentage_Share_pct
FROM main_data m
JOIN dim_transport t 
    ON m.Transport_Mode = t.Transport_Mode
GROUP BY 
    t.Transport_Mode
ORDER BY 
    Total_Arrivals DESC;

/* ============================================================================
   6- Overall KPIs Summary (2005-2024)
   ============================================================================ */
SELECT 
   
    ROUND(SUM(Tourist_Arrivals) / 1000000, 1) AS Total_Arrivals_Million,
    ROUND(SUM(Tourism_Revenue_USD) / 1000000000, 1) AS Total_Revenue_Billion_USD,
    ROUND(AVG(Avg_Spend_Per_Tourist_USD), 0) AS Average_Spend_USD,
    ROUND(AVG(Hotel_Occupancy_Rate_pct), 1) AS Average_Occupancy_Rate_pct
FROM main_data;
    