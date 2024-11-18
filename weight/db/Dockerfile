FROM mysql:5.7
# Set environment variables for MySQL
# Need Secure the MYSQL password
ENV MYSQL_ROOT_PASSWORD=123
ENV MYSQL_DATABASE=weight
EXPOSE 3306
# Change the MySQL port to 5001 using a custom entrypoint
copy weightdb.sql /docker-entrypoint-initdb.d/weightdb.sql

CMD ["mysqld", "--port=5001"]
