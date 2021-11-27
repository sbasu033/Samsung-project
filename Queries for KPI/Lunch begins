with cte as
(select cast(Time as date)[Date], *, ROW_NUMBER() OVER (PARTITION BY cast(Time as date) ORDER BY Time ASC) AS rn 
from [cairo].[dbo].[data - Copy]
where cast(Time as time) between '12:00:00.000' and '13:00:00.000'  
and (sensor ='M021' or sensor = 'M024') and status = 'ON'
)
select Date,cast(Time as time)[Time], 'Lunch begins expected' as KPI_expected
from cte
where rn=1
