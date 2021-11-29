with cte as
(select cast(Time as date)[Date], *, ROW_NUMBER() OVER (PARTITION BY cast(Time as date) ORDER BY Time ASC) AS rn 
from [cairo].[dbo].[data - Copy]
where cast(Time as time) between '13:00:00.000' and '13:30:00.000'  
and (sensor ='M021' or sensor = 'M024' or sensor = 'M022') and status = 'OFF'
)
select Date,cast(Time as time)[Time], 'Lunch ends expected' as KPI_expected
from cte
where rn=1
