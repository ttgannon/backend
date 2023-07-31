-- write your queries here

--1
SELECT * FROM owners FULL JOIN vehicles ON owners.id = vehicles.owner_id;

--2
SELECT first_name, last_name, COUNT(*) AS count FROM owners JOIN vehicles ON owners.id = vehicles.owner_id GROUP BY first_name, last_name ORDER BY count ASC;

--3
SELECT first_name, last_name, ROUND(AVG(price)) 
AS average_price, COUNT(*) AS count 
FROM owners 
JOIN vehicles ON owners.id = vehicles.owner_id 
GROUP BY first_name, last_name 
HAVING AVG(price) > 10000 AND COUNT(*) > 1
ORDER BY first_name DESC;