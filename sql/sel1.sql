use hotels;
select source, COUNT(*) from hotel_info where date_scraped = convert(char(10), GETDATE(), 101) 
	group by source;